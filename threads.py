import re
import m5
import os
from m5.objects import *
from m5.stats import *

m5.util.addToPath("../gem5/configs/common")
import SimpleOpts
from caches import *

# Binary to execute
binaryfile = "hello"
thispath = os.path.dirname(os.path.realpath(__file__))
default_binary = os.path.join(thispath, binaryfile)
SimpleOpts.add_option("--binary", nargs="?", default=default_binary)
SimpleOpts.add_option("--num_threads", nargs="?", type=int, default=2)  # Allow setting thread count from CLI
args = SimpleOpts.parse_args()

print(thispath)

# Create the system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "3GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("8192MiB")]

# Configure a multi-threaded CPU
system.cpu = DerivO3CPU()
system.cpu.numThreads = args.num_threads  # Set the number of threads dynamically

# Configure superscalar parameters
system.cpu.fetchWidth = 8
system.cpu.decodeWidth = 8
system.cpu.renameWidth = 8
system.cpu.dispatchWidth = 8
system.cpu.issueWidth = 8
system.cpu.commitWidth = 8

# Create L1 instruction and data cache
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create L2 cache and memory bus
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache(args)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

# Interrupt Controller
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

# Create memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(args.binary)

# ================= Multi-threading Configuration =================
# Create multiple processes for multi-threaded execution
processes = []
for i in range(args.num_threads):
    process = Process()
    process.cmd = [args.binary]
    processes.append(process)

system.cpu.workload = processes  # Assign multiple processes to the CPU
system.cpu.createThreads()  # Initialize thread contexts
# ================================================================

# Root system setup and simulation
root = Root(full_system=False, system=system)
m5.instantiate()
m5.stats.reset()

print(f"\n======================================================")
print(f"Beginning simulation with {args.num_threads} threads!")
print(f"======================================================\n")

exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")

m5.stats.dump()  # Dump collected statistics
m5.stats.reset()

print(f"======================================================")
print(f"End of Simulation!")
print(f"======================================================\n")
