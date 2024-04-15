module DataMemory (
    input wire clk,      // Clock signal
	 input wire [7:0] addr,
    output reg [Memory_WIDTH-1:0] data_out, // Output data
	 input wire [1:0] Command,				
	 input wire Memory_add	
);

parameter Memory_WIDTH = 8192;

reg [Memory_WIDTH-1:0] memory;
reg [11:0] mem_addr;


always@ (posedge clk) begin
	
	if(Memory_add) begin
		mem_addr = {addr, 5'b0};
		memory[mem_addr +: 8] <= memory[mem_addr +: 8] + 1'b1;
	end

	if(Command == 2'b01) begin
		memory <= {Memory_WIDTH{1'b0}};
	end 
	
	data_out <= memory;

end


endmodule

