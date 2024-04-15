module DataMemory (
    input wire clk,      // Clock signal
	 input wire [6:0] addr,
    output reg [8191:0] data_out, // Output data
	 input wire [1:0] Command
);

reg [8191:0] memory;



endmodule

