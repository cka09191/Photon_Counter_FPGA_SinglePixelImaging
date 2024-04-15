module counter_32bit(
  input wire clk50Mhz,
  input wire sig,
  input wire rst,
  output reg [31:0] cnt=0
  );
  
 reg [31:0] cnt1=0;
 reg [31:0] cnt2=0;
 reg [31:0] cnt3=0;
 reg [31:0] cnt4=0;
 reg [31:0] cnt5=0;
 reg [31:0] cnt6=0;
 reg [31:0] cnt7=0;
 reg [31:0] cnt8=0;
 reg [31:0] cnt9=0;
 reg [31:0] cnt10=0;
 reg [31:0] cnt11=0;
 reg [31:0] cnt12=0;
 reg [31:0] cnt13=0;
 reg [31:0] cnt14=0;
 reg [31:0] cnt15=0;
 reg [31:0] cnt16=0;
 reg [31:0] cnt17=0;
 reg [31:0] cnt18=0;
 reg [31:0] cnt19=0;
 reg [31:0] cnt20=0;
/*always@(posedge rst) cnt <= 0;*/
 
always@(posedge clk50Mhz) begin
	if(~rst) begin 
		if(sig) cnt <= cnt + 1; end
	else cnt<= 0; 
end	


endmodule
