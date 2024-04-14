module plot_distributer(
	input wire clk,
	input wire [7:0] START_END_INTERVAL,
	output reg [6:0] Addr
);


reg START = START_END_INTERVAL[7];
reg END = START_END_INTERVAL[6];
reg [5:0] INTERVAL = START_END_INTERVAL[5:0];

endmodule
