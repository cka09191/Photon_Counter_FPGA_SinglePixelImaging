module DataMemory (
    input wire clk,      // Clock signal
    input wire rst,      // Reset signal
	 
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
always@(negedge rst) begin
	if(addr == 10'b10000000) Signal <= 1;
	else begin 
		memory[addr] <= data_in;
		addr <= addr + 1;
		end
end

// Memory Output
always@(posedge clk) begin
	if(Signal) begin
		if(addr == 0) Signal <= 0;
		else begin 
			data_out <= memory[addr];
			addr <= addr-1;
			end
		end
end


endmodule
