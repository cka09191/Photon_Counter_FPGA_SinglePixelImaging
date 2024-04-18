module DataMemory (
   input wire clk,      // Clock signal
	 input wire [6:0] addr,
   output reg [31:0] data_out, // Output data
	 input wire [1:0] Command,				
	 input wire Memory_add	
);



reg [31:0] memory [0:127];
//reg [12:0] mem_addr = 0;
integer i;
reg [7:0] r_addr = 0;
reg [7:0] r_addr2 = 0;



always@ (posedge clk) begin


/*
	if(Command == 2'b01) begin
		for (i = 0; i < 128; i = i + 1) begin
        memory[i] = 32'b0; // Assign 0 to each memory location
      end
	end else */if(Memory_add) begin
		
		//memory[addr] = memory[addr] + 1;
		r_addr = {1'b0,addr};
		data_out[15:8] <= r_addr;
	end else begin
		r_addr2 = r_addr2+1;
		data_out[31:16] <= 0;
		data_out[7:0] <= r_addr2;
	end
	

end

endmodule


