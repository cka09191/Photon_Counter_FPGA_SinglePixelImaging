
module plot_distributer(
	input wire clk,
	input wire [1:0] START,
	input wire [1:0] END,
	input wire [6:0] INTERVAL,
	input wire data_arrived,
	output reg [7:0] Addr,
	output reg Memory_add
);

parameter address_0 = 7'd128;
reg [3:0] count = 0;

/*
always @(posedge clk) begin
	if (Memory_add == 1'b1) begin
		count <= count + 1;
		if(count == 5) begin
			Memory_add <= 1'b0;
			count <= 0;
		end
	end
end
*/

always @(posedge data_arrived) begin
	if(START == 2'b00 && END == 2'b11 && INTERVAL == 7'b0000000) begin
		Addr <= address_0;
		Memory_add <= 1'b1;
	end
	else if(START == 2'b01 && END == 2'b10) begin
		Addr <= address_0 + INTERVAL;
		Memory_add <= 1'b1;
	end
	else if(START == 2'b10 && END == 2'b01) begin
		Addr <= address_0 - INTERVAL;
		Memory_add <= 1'b1;
	end
end
endmodule
