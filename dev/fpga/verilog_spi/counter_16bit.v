module counter_16bit(
  input wire clk50Mhz,
  input wire rst,
  input wire sig,
  output reg [15:0] cnt=0
  );
  
 
always@(posedge rst) cnt <= 0;
 
always@(posedge clk50Mhz) begin 
	if(sig) cnt <= cnt + 1;
end	



 endmodule
