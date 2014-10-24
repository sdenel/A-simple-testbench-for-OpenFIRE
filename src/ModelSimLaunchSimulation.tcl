#
# This tcl script 
#

cd YOUR_CURRENT_DIRECTORY_HERE
set OF_DIR ../OPENFIRE_DIRECTORY/trunk/rtl

quit -sim
vdel -all -lib work
vlib work

# Initializing memory
python3 memory_init.py

# Loading OpenFIRE
vlog +incdir+$OF_DIR $OF_DIR/openfire_arbitrer.v $OF_DIR/openfire_cpu.v $OF_DIR/openfire_decode.v $OF_DIR/openfire_execute.v $OF_DIR/openfire_fetch.v $OF_DIR/openfire_iospace.v $OF_DIR/openfire_pipeline_ctrl.v  $OF_DIR/openfire_primitives.v $OF_DIR/openfire_regfile.v $OF_DIR/openfire_soc.v

# Loading the testbench
vlog simulation.v

vsim work.Test_openFIRE
# Set in nanoseconds
configure wave -timelineunits ns
# Basis = 10ns (100Mhz)
configure wave -gridperiod 10ns
configure wave -valuecolwidth 10
add wave -position end  sim:/Test_openFIRE/clock
add wave -position end  sim:/Test_openFIRE/reset
add wave -divider {Bus data}
add wave -position end -radix hexadecimal sim:/Test_openFIRE/dmem_addr
add wave -position end -radix decimal sim:/Test_openFIRE/dmem_data_in
add wave -position end -radix decimal sim:/Test_openFIRE/dmem_data_out
add wave -position end sim:/Test_openFIRE/dmem_re
add wave -position end sim:/Test_openFIRE/dmem_we
add wave -position end sim:/Test_openFIRE/dmem_input_sel
add wave -position end sim:/Test_openFIRE/dmem_done
add wave -divider {Bus instructions}
add wave -position end -radix hexadecimal sim:/Test_openFIRE/imem_addr
add wave -position end -radix hexadecimal sim:/Test_openFIRE/imem_data_in
add wave -position end -radix ascii sim:/Test_openFIRE/imem_data_in_comments
add wave -position end sim:/Test_openFIRE/imem_re
add wave -position end sim:/Test_openFIRE/imem_done
run 150ns
