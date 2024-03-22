module counter_16bit(
  input wire clk50Mhz,
  input wire rst,
  input wire sig,
  output reg [15:0] cnt=0
  );
   
always@(posedge clk50Mhz or posedge rst)
  
begin
  
  if(rst) begin 
  
  cnt <= 1'b0; 
  end 

  else if(sig) begin cnt <= cnt + 1; end 

  end

 endmodule
