module controller(
	input wire clk,
	input wire button,
	output reg [1:0] cnt
);

reg check = 0;
re
always@ (posedge clk) begin
	
	if(button==1 && check==0) begin
		cnt <= cnt + 1;
		check <= 1;
	end else if (button ==0 && check==1) begin
		check <= 0;
	end
	
	if(cnt > 3'b11) cnt <= 0; 
	
end

endmodule 