module DataMemory (
    input wire clk,      // Clock signal
	 input wire [6:0] addr,
    output reg [Memory_WIDTH-1:0] data_out, // Output data
	 input wire [1:0] Command,
	 input wire Memory_add
);

parameter Memory_WIDTH = 8192;

reg [Memory_WIDTH-1:0] memory;
reg [11:0] mem_addr;

always@ (posedge clk) begin
	 reg [9:0] mem_addr;
    mem_addr = {addr, 5'b0}; // Concatenate addr with zeros for bit shifting
	 memory[mem_addr +: 8] <= memory[mem_addr +: 8] + 1'b1; // Use part-select operator
	if(Command == 2'b01) begin
		data_out <= {Memory_WIDTH{1'b0}};
	end
end	


endmodule

