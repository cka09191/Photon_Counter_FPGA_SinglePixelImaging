
module plot_distributer(
	input wire clk,
	input wire [1:0] START,
	input wire [1:0] END,
	input wire [5:0] INTERVAL,
	input wire data_arrived,
	output reg [6:0] Addr = 0,
	output reg Memory_add = 0
);

reg [2:0] data_arrived_r;  always @(posedge clk) data_arrived_r <= { data_arrived_r[1:0], data_arrived };
wire data_arrived_rising  = ( data_arrived_r[2:1] == 2'b01 );
parameter address_0 = 64;
reg [3:0] count = 0;

reg add_internal = 0;


always @(posedge clk) begin
	if (Memory_add == 1'b1) begin
		if(count == 5) begin
			Memory_add <= 1'b0;
			count <= 0;
		end
		else begin
			count <= count + 1;
			Memory_add <= 1'b1;
		end
	end
	else count <= 0;
	if(data_arrived_rising) begin
		if(START == 2'b00 && END == 2'b11 && INTERVAL == 6'b000000) begin
			Addr <= address_0;
			Memory_add <= 1'b1;
			count<=0;
		end
		else if(START == 2'b01 && END == 2'b10) begin
			Addr <= address_0 + INTERVAL;
			Memory_add <= 1'b1;
			count<=0;
		end
		else if(START == 2'b10 && END == 2'b01) begin
			Addr <= address_0 - INTERVAL;
			Memory_add <= 1'b1;
			count<=0;
		end
	end
end
endmodule
