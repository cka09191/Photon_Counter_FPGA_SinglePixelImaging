module counter_8bit(
  input wire clk50Mhz,
  input wire rst,
  input wire sig,
  output reg [7:0] cnt
  );
   
always@(posedge clk50Mhz or posedge rst)
  
begin
  
  if(rst) cnt <= 1'b0; 

  else if(sig) cnt <= cnt + 1; 

  end

 endmodule
