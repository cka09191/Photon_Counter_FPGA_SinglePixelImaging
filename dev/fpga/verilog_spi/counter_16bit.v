module counter_16bit(
  input wire clk50Mhz,
  input wire DMD_sig,
  input wire sig,
  input wire rst,
  output reg [15:0] cnt=0
  );
   
always@(posedge clk50Mhz or posedge rst)
  
begin
  
  if(rst) cnt <= 0;

  else if(sig) cnt <= cnt + 1; 

  end

 endmodule
