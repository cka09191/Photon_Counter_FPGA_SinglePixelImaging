module DataMemory (
    input wire clk,      // Clock signal
    input wire RD,      // Reset signal
	 input wire DMD_sig,
	 input wire [15:0] data_in,
    output reg [15:0] data_out // Output data
);

// Define memory to store 255 pieces of data
reg [15:0] memory [0:1023];

// Address register to read data from memory
reg [9:0] addr = 0;

reg Signal = 0;

// Output register to hold data to emit
reg [15:0] output_data;

// Memory Input
/*always@(posedge clk) begin
	
end*/

// Memory Output
always@(posedge clk) begin
	if(DMD_sig) memory[addr] <= data_in ;
end


endmodule
