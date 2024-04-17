module delay(
	input wire clk,
	input wire [1:0] cnt,
	input wire pulse,
	output reg pulse2
);

reg [1:0] count=0; 
assign pusle2 = 0;

always@ (posedge clk) begin
	if(count > cnt) begin
		pulse2 <= 1;
		cnt <= 0;
	end else begin
		cnt <= cnt + 1;
	end
end