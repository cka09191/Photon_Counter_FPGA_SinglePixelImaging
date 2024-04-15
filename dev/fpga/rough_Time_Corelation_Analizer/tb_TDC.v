`timescale 1ns / 1ps

module tb_TDC;

  // Parameters
  reg pulse1;
  reg pulse2;
  reg clk;
  wire [1:0] START_signal;
  wire [1:0] END_signal;
  wire [6:0] INTERVAL;
  wire data_arrived;

  // Instantiate the TDC module
  TDC u1 (
    .pulse1(pulse1),
    .pulse2(pulse2),
    .clk(clk),
    .START_signal(START_signal),
    .END_signal(END_signal),
    .INTERVAL(INTERVAL),
    .data_arrived(data_arrived)
  );

  // Clock generator
  always begin
    #1 clk = ~clk;
  end

  // Test sequence
  initial begin
    $dumpfile("tb_TDC.vcd");
    $dumpvars(0, tb_TDC);
    clk = 0;
    pulse1 = 0;
    pulse2 = 0;
    #10 pulse1 = 1;
    #1 pulse1 = 0;
    #10 pulse2 = 1;
    #1 pulse2 = 0;
    #100 pulse1 = 1;
    #1 pulse1 = 0;
    #10 pulse2 = 0;
    #1 pulse2 = 0;
    #100pulse2 = 1;
    #1 pulse2 = 0;
    #10 pulse1 = 1;
    #1 pulse1 = 0;
    #1 pulse2 = 0;
    #10 pulse1 = 1;
    #1 pulse1 = 0;
    #100 pulse2 = 1;
    #1 pulse2 = 0;
    #50 $finish;
  end

endmodule