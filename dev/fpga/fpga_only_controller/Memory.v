module DataMemory (
    input wire clk,      // Clock signal
    input wire RD,      // Reset signal
	 input wire DMD_sig,
	 input wire [15:0] data_in,
	 input wire rxValid,
    output reg [15:0] data_out // Output data
);

// Define memory to store 255 pieces of data
reg [15:0] memory [0:1023];

// Address register to read data from memory
reg [9:0] addr = 1;

reg Signal = 0;

// Output register to hold data to emit
reg [15:0] output_data;

reg [2:0] DMD_sig_r;  always @(posedge clk) DMD_sig_r <= { DMD_sig_r[1:0], DMD_sig };
reg [2:0] RD_r;    always @(posedge clk) RD_r  <= {   RD_r[1:0],  RD };
wire DMD_sig_rising  = ( DMD_sig_r[2:1] == 2'b01 );
wire DMD_sig_falling = ( DMD_sig_r[2:1] == 2'b10 );
wire RD_rising =  ( RD_r[2:1] == 2'b10 );
wire RD_falling   = ( RD_r[2:1] == 2'b10 );

initial begin
	memory[0] = 0;
end

always@(posedge clk) begin
	
	if(DMD_sig_rising) memory[addr] <= data_in ;
	else if(DMD_sig_falling) addr = addr + 1;
	
	if(RD) begin 
		if(rxValid) data_out <= memory[addr];
		else addr = addr - 1;
	end
end


endmodule

