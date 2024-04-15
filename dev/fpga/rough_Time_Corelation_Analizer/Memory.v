module DataMemory (
    input wire clk,      // Clock signal
	 input wire [6:0] addr,
    output reg [Memory_WIDTH-1:0] data_out, // Output data
	 input wire [1:0] Command,
	 input wire Memory_add
);

parameter Memory_WIDTH = 8192;

reg [Memory_WIDTH-1:0] memory;

always@ (posedge clk) begin
	memory[32*addr:32*addr+7] <= memory[32*addr:32*addr+7] + 1'b1;
	if(Command == 2'b01) begin
		data_out <= {Memory_WIDTH{1'b0}};
	end
end	


endmodule

