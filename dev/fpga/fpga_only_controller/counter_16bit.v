module counter_16bit(
  input wire clk50Mhz,
  input wire DMD_sig,
  input wire sig,
  input wire rst,
  output reg [15:0] cnt=0
  );
  
 
/*always@(posedge rst) cnt <= 0;*/
 
always@(posedge clk50Mhz) begin
	if(~rst)	
		if(DMD_sig) cnt <= 0;
		else begin 
		  if(sig) cnt <= cnt + 1;
		end
end	



 endmodule
