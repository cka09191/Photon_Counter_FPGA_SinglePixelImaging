module tb_counter();
  
reg clk;
reg RD;
reg DMD_sig;
reg rst;
reg sig;
wire [15:0] cnt;
wire [15:0] data_out;

DataMemory Memory1(
  .clk(clk),
  .RD(RD),
  .DMD_sig(DMD_sig),
  .data_in(cnt),
  .data_out(data_out)
);

counter_16bit count1(
  .clk50Mhz(clk),
  .DMD_sig(DMD_sig),
  .sig(sig),
  .rst(rst),
  .cnt(cnt)
);

initial begin
  clk = 0;
  rst = 0;
  sig = 0;
  DMD_sig = 0;
  RD = 0;
end

always #5 clk = ~clk;

always #10 sig = ~sig;
 
always begin
 #250 DMD_sig =~DMD_sig;
 #10 DMD_sig=~DMD_sig;
 #100 DMD_sig =~DMD_sig;
 #10 DMD_sig=~DMD_sig;
end

always@(posedge DMD_sig) begin
  $display("%b",data_out);
end

initial begin
  rst = 1;
  #10000;
  rst = 0;
end

endmodule




