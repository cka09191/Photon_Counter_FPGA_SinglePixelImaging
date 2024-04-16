module DataMemory (
   input wire clk,      // Clock signal
	 input wire [7:0] addr,
   output reg [8191:0] data_out, // Output data
	 input wire [1:0] Command,				
	 input wire Memory_add	
);

parameter Memory_WIDTH = 8192;

reg [Memory_WIDTH-1:0] memory = 0;
reg [12:0] mem_addr = 0;


always@ (posedge clk) begin
	
	if(Memory_add) begin
		mem_addr = {addr, 5'b0};
		memory[mem_addr +: 8] <= memory[mem_addr +: 8] + 1'b1;
		data_out <= memory;
	end

	if(Command == 2'b01) begin
		memory <= {Memory_WIDTH{1'b0}};
		data_out <= memory;
	end 
	
	

end


endmodule


