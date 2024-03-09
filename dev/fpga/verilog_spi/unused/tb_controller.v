`timescale 1ns/1ps
module tb_controller;
    reg CLK;
    reg [7:0] COMMAND;
    reg start_clk = 0;
    wire START_COUNT;

    controller uut (
        .CLK(CLK), 
        .COMMAND(COMMAND), 
        .START_COUNT(START_COUNT)
    );

    initial begin
        $dumpfile("tb_controller.vcd");
        $dumpvars(0, tb_controller);
        $display("start");
        CLK = 0;
        start_clk = 0;
        COMMAND = 0;
        $display("0tick");
        #1;
        $display("1tick");
        start_clk = 1;
        #10;
        $display("10tick");
        COMMAND = 1;
        #100;
        COMMAND = 0;
        #100;
        COMMAND = 1;
        #100;
        COMMAND = 0;
        start_clk = 0;
        #100;
        COMMAND = 1;
        #100;
        start_clk = 1;
        #100;
        start_clk = 0;
        COMMAND = 0;
        #100;

        $finish;
    end

    always begin
        #1;
        if (start_clk == 1) begin
            CLK <= ~CLK;
        end
    end
endmodule