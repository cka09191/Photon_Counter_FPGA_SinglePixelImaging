module tb_cnt();
  
  reg clk50Mhz = 1'b0;
  reg rst = 1'b1;
  reg sig = 1'b0;
  wire [7:0] cnt;
  
counter_8bit cnt2(
  .clk50Mhz(clk50Mhz),
  .rst(rst),
  .sig(sig),
  .cnt(cnt)
  );
   
  always #20 clk50Mhz = ~clk50Mhz;


  always #30 sig = ~sig;
  
  initial begin 
  rst=1'b1;
  #10; rst=1'b0; #1000; rst=1'b1;
  end


 endmodule
