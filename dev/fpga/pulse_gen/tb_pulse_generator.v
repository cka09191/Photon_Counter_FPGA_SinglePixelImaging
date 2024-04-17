`timescale 1ns/1ps

module tb_pulse_generator;

    // Parameters
    reg clk;
    reg pulse_clk;
    reg [7:0] delay;
    wire pulse1;
    wire pulse2;

    // Instantiate the Unit Under Test (UUT)
    pulse_generator uut (
        .clk(clk), 
        .pulse_clk(pulse_clk), 
        .delay(delay), 
        .pulse1(pulse1), 
        .pulse2(pulse2)
    );

    initial begin
        $dumpfile("tb_mini_test.vcd");
        $dumpvars(0, tb_mini_test);
        // Initialize Inputs
        clk = 0;
        pulse_clk = 0;
        delay = 8'd0;

        // Toggle clock every 2.5ns (for a 400MHz clock)
        forever #2.5 clk = ~clk;
    end
    initial begin
        forever #1000 pulse_clk = ~pulse_clk;
    end

    initial begin
        // Testbench Code
        #10 delay = 8'd5;
        #50000 delay = 8'd10;
        #1000000
        #30 $finish;
    end

endmodule