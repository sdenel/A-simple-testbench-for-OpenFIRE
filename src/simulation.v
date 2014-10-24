// Simple verilog simulation of an openFIRE core
// instantiated without fsl nor interruptions

`timescale 1ns/1ns
module Test_openFIRE;

reg  clock, reset;
wire [31:0] dmem_addr;
reg  [31:0] dmem_data_in;
wire [31:0] dmem_data_out;
wire dmem_we;
wire dmem_re;
wire [1:0] dmem_input_sel;
reg  dmem_done;
wire [31:0] imem_addr;
reg  [31:0] imem_data_in;
wire imem_re;
reg  imem_done;

reg [31:0] memory [0:4095];
initial $readmemh("memory.txt", memory);
reg [800:0] memory_comments [0:100];
initial $readmemh("memory_comments.txt", memory_comments);
reg [800:0] imem_data_in_comments;

// Instantie openFIRE
openfire_cpu openfire_cpu(
	clock,		reset,
	dmem_addr, 	dmem_data_in,	dmem_data_out,
	dmem_we, 	dmem_re,	dmem_input_sel,		dmem_done,
	imem_addr,	imem_data_in,	imem_re, 		imem_done
);


initial begin
	clock = 1'b1;
	reset = 1'b1;
	
	dmem_done = 1'b0;
	imem_done = 1'b0;
	
	#15 reset = 1'b0;
end

always #5 clock = ~clock;

// Simulating a "perfect" memory
// The simulated memory is reading/writing the data in less than a clock tick
always @(posedge ~clock) begin
	if(~reset) begin
		if(imem_re) begin
			imem_data_in <= memory[imem_addr>>2];
			imem_data_in_comments <= memory_comments[imem_addr>>2];
			imem_done <= 1;
		end
		else begin
			imem_done <= 0;
		end
		if(dmem_re) begin
			dmem_data_in <= memory[dmem_addr>>2];
			dmem_done <= 1;
		end
		else if(dmem_we) begin
			memory[dmem_addr>>2] <= dmem_data_out;
			dmem_done <= 1;
		end
		else begin
			dmem_done <= 0;
		end
		

	end
end
always @(posedge ~clock) begin
	if(~reset) begin

	end
end

endmodule
