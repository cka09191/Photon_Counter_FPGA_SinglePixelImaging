module Command(
	input wire clk,
	input wire [8191:0] rx,
	output reg [1:0] Command,
	input wire rxValid
);

always@ (posedge clk) begin
	if(rxValid) begin
	   if (rx == 8192'hFF) Command <= 2'b01;
	end else Command <= 2'b00;
end

endmodule