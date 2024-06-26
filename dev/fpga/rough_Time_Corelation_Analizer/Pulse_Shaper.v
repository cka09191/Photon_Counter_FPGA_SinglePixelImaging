module Pulse_Shaper(
	input wire clk,// 500MHz
	input wire channel,
	output reg pulse
);

reg [7:0] count; // 8 bit counter for dead time:60ns, pulse width:2ns
reg activate;

initial begin
    activate = 0;
    count = 8'd127;
	pulse <= 0;
end



always @(posedge clk) begin
	if(activate) begin
		case(count)
<<<<<<< HEAD
			8'd10: begin
				count<= count+1;
				pulse<=0;
			end
			8'd30: begin
=======
			8'd20: begin
>>>>>>> 512b425b67d8c3ff3cd7d3016c1330d3e7d46c6c
				activate = 0;
				count = 8'h00;
			end
			default: begin
				count <= count + 1;
				pulse <= pulse;
			end
		endcase
	end
	else begin
		if(channel) begin 
			activate=1;
			pulse <= 1;
		end
	end
end

endmodule
