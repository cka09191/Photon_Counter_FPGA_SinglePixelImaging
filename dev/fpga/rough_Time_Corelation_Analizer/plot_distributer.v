module plot_distributer(
	input wire clk,
	input wire START,
	input wire END,
	input wire [5:0] INTERVAL,
	input wire data_arrived,
	output reg [6:0] Addr,
	output reg Memory_add
);

parameter address_0 = 128;

endmodule
