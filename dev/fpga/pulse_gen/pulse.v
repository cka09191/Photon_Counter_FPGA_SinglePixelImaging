module pulse(
	input wire clk400Mhz,
	input wire clk1Mhz,
	output reg pulse
);

reg [2:0] count; // 8 bit counter for dead time:60ns, pulse width:2ns
reg Up_pulse;



initial begin
    Up_pulse = 0;
    count = 3'b000;
	 pulse <= 0;
end

always@ (posedge clk400Mhz) begin
	if(Up_pulse) begin 
		if(count==3'b111) begin
			pulse <= 0;
			count <= 0;
			Up_pulse <= 0;
		end else begin
			count <= count + 1;
		end
	end
	else if(clk1Mhz) begin 
		pulse <= 1;
		Up_pulse <= 1;
	end

end

endmodule