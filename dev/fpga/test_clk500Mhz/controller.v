module controller(
	input wire clk,
	input wire rxValid,
	input wire [31:0] rx,
	output reg [31:0] tx
);

reg [31:0] rx_buffer = 32'bxxxxxxx;

always@ (posedge clk) begin
	if (rxValid) begin
		rx_buffer <= rx;
	end
end

always@ (posedge clk) begin
	case (rx_buffer)
		32'hFFFF_FFFF: tx <= 32'h1111_1111;
		32'hEEEE_EEEE: tx <= 32'h2222_2222;
		32'hDDDD_DDDD: tx <= 32'h3333_3333;
		32'hBBBB_BBBB: tx <= 32'h4444_4444;
		default: tx <= 32'h0000_0000;
	endcase

end

endmodule