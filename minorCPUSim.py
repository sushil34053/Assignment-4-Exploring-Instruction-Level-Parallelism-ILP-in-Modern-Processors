import m5
from m5.objects import *

m5.util.addToPath("../gem5/src/cpu/minor")
import minorCPU

m5.util.addToPath("../gem5/src/mem")
import SimpleOpts

# Create a system
system = System()

# Set up the clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'  # 1 GHz clock
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the memory system
system.mem_mode = 'timing'  # Use timing mode for memory
system.mem_ranges = [AddrRange('512MiB')]  # Use MiB to avoid warning

# Create a CPU
system.cpu = MinorCPU()  # Use MinorCPU model

# Create a memory bus
system.membus = SystemXBar()

# Connect the CPU to the memory bus
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Connect the system port (for global memory access)
system.system_port = system.membus.cpu_side_ports

# Create a memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()  # Use DDR3 memory
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Set up the process (run a simple binary)
process = Process()
process.cmd = ['./hello']  # Use a valid binary (e.g., compiled "Hello World")
system.cpu.workload = process
system.cpu.createThreads()

# Set up the root system
root = Root(full_system=False, system=system)

# Instantiate the system
m5.instantiate()

# Run the simulation
print("Starting simulation!")
exit_event = m5.simulate()

# Print the reason for the simulation exit
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")