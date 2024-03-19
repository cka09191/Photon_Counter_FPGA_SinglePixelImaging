module counter_8bit(
  input wire clk50Mhz,
  input wire rst,
  input wire sig,
  output reg [7:0] send_data=0,
  output reg write_en=0	
  );
   
reg [7:0] cnt = 3'hxxx;

	
always@(posedge clk50Mhz or posedge rst)
  
begin
  
  if(rst) begin
  send_data <= cnt;
  write_en <= 1;
  cnt <= 1'b0; 
  end 

  else if(sig) begin 
  write_en <= 0;
  cnt <= cnt + 1; 
  end 

  end

 endmodule
