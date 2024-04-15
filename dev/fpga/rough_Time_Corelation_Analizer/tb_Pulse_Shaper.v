`timescale 1ns/1ps

module tb_Pulse_Shaper;

    reg clk;
    reg channel;
    wire pulse;

    // Instantiate the Pulse_Shaper
    Pulse_Shaper uut (
        .clk(clk),
        .channel(channel),
        .pulse(pulse)
    );

    // Clock generator
    always begin
        #1 clk = ~clk;
    end

    // Test sequence
    initial begin
        // Initialize signals
        $dumpfile("tb_Pulse_Shaper.vcd");
        $dumpvars(0, tb_Pulse_Shaper);
        clk = 0;
        channel = 0;

        // Apply test vectors
        #10 channel = 1; // Trigger pulse
        #20 channel = 0; // Stop pulse
        #500 channel = 1; // Trigger pulse again
        #1 channel = 0; // Stop pulse again
        #1 channel = 1; // Trigger pulse again
        #1 channel = 0; // Stop pulse again
        #1 channel = 1; // Trigger pulse again
        #1 channel = 0; // Stop pulse again
        #1 channel = 1; // Trigger pulse again
        #1 channel = 0; // Stop pulse again
        #1 channel = 1; // Trigger pulse again
        #1 channel = 0; // Stop pulse again
        #1 channel = 1; // Trigger pulse again
        #1 channel = 0; // Stop pulse again

        // End of test
        #40 $finish;
    end

    // Monitor
    initial begin
        $monitor("At time %d, channel = %b, pulse = %b", $time, channel, pulse);
    end

endmodule