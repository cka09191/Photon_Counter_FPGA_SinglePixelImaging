module Pulse_Shaper(
	input wire clk,// 500MHz
	input wire channel,
	output reg pulse
);

reg [7:0] count; // 8 bit counter for dead time:60ns, pulse width:2ns
reg activate;

initial begin
    activate = 0;
    count <= 8'h00;
	pulse <= 0;
end

always @(posedge channel) begin
    if(channel) begin
        activate <= 1;
    end
end

always @(posedge clk) begin
	if(activate) begin
		count[7:0] <= count + 1;
		case(count)
			8'd0: pulse <= 1;
			8'd30: begin
				pulse <= 0;
				activate <= 0;
				count <= 8'h00;
			end
			default: pulse <= 0;
		endcase
	end
end

endmodule
