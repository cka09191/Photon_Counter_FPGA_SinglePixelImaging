`timescale 1ns/1ps
module tb_counter_16bit;
    reg CLK;
    wire [15:0] cnt;
    reg start_clk = 0;
    reg rst = 0;
    reg sig;

    counter_16bit uut (
        .clk50Mhz(CLK), 
        .rst(rst), 
        .cnt(cnt),
        .sig(sig)
    );
    always begin
        #1;
        if (start_clk == 1) begin
            CLK <= ~CLK;
        end
    end
    initial begin
        $dumpfile("tb_counter_16bit.vcd");
        $dumpvars(0, tb_counter_16bit);
        $display("start");
        CLK = 0;
        start_clk = 0;
        sig = 1;
        $display("0tick");
        #1;
        $display("1tick");
        start_clk = 1;
        #10;
        $display("10tick");
        #100;
        rst = 1;
        #100;
        rst= 0;
        #100;
        start_clk = 0;
        #100;
        rst= 0;
        #100;

        rst= 1;
        start_clk = 1;
        #100;
        start_clk = 0;
        #100;

        $finish;
    end

endmodule