A simple testbench for OpenFIRE

A simple testbench for the RISC, tiny and opensource softprocessor called OpenFIRE.

OpenFIRE is a RISC softcore processor available on OpenCores and written in Verilog. It has the same instruction set than the Xilinx MicroBlaze processor, and is therefore compatible with a well-maintained toolchain. It can be seen both like a computing resource and like an IP. This is why I suggest here to stimulate it with assembly instructions transformed in binary, and see the result with ModelSim. Are you in a hurry? Then let's just see the result.

Principle
---------

This simulation is composed of 3 files. The data variable in the memory_init.py script must contain your simple program, written in assembler. Currently, it is:

    ADDI R1,R0,1024 # R1 <- Add(A)=0x100
    LW R2,R0,R1     # Chargement dans R2 de A=5 stocké à l'adresse 0x100
    ADDI R1,R1,4    # R1 <- Add(B)=Add(A)+4bytes
    LW R3,R0,R1     # Chargement dans R2 de A=5 stocké à l'adresse 0x100
    ADD R2,R2,R3    # R2<-5+1=6
    MUL R4,R2,R2    # R2<-R2*R2
    SW R4,R0,R1     # Sauvegarde de R2 à l'adresse 0x100

 

The script will automatically remove comments and transform the assembly code to their binary equivalent, as defined in the MicroBlaze Processor Reference Guide. These data are used by a simulated memory module included in simulation.v. The assembly code is kept in a readable form and put in another memory that will be read by the testbench at the same time than instructions, giving a more pleasant view with ModelSim.
simulation.v instanciates both these simulated memory, initialized by txt files created by the python script, and the processor. Once the reset signal is put down, the processor requires the data at address 0x0 and so on, and this is where the program was stored.
Source code

Source files are shown and highlighted below, but are nevertheless available here.
The verilog testbench
Show/Hide TestBench.v
The Python script instanciating OpenFIRE and simulated memories
Show/Hide memory_init.py
The ModelSim initialization file

This file must be executed (you can also copy its content) in ModelSim.
Show/Hide launchSim.tcl
The final result
Running these scripts will give you this output:
A simple simulation of OpenFIRE with ModelSim (click to enlarge)
Others
The RISC OpenFIRE main page: http://opencores.org/project,openfire2
Installing the cross-compilation tool for OpenFIRE (and Microblaze): as OpenFIRE is using the same instruction set than the Xilinx MicroBlaze processor, tools from Xilinx can be used to compile your programs. The installation procedure can be found here: http://wiki.xilinx.com/mb-gnu-tools'>http://wiki.xilinx.com/mb-gnu-tools. It may require up download 1.5GiB, but you can remove somes directories like binaries/ and sub-directories not aimed for your distribution. It will afterwards require less than 200MiB for the entire toolchain.


