module Command(
	input wire clk,
	input wire [4095:0] rx,
	output reg [1:0] Command,
	input wire rxValid
);

always@ (posedge clk) begin
	if(rxValid) begin
	   if (rx == 4096'hFF) Command <= 2'b01;
	end else Command <= 2'b00;
end

endmodule