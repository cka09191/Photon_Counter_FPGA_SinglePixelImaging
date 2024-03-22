`timescale 1ns/1ps
module tb_counter_16bit;
    reg CLK=0;
    wire [15:0] cnt;
    reg start_clk = 0;
    reg rst = 0;
    reg sig=0;

    counter_16bit uut (
        .clk50Mhz(CLK), 
        .rst(rst), 
        .cnt(cnt),
        .sig(sig)
    );
    always begin
        #2;
        if (start_clk == 1) begin
            CLK <= ~CLK;
        end
    end
    always begin
        #2;
        sig = ~sig;
    end
    initial begin
        $dumpfile("tb_counter_16bit.vcd");
        $dumpvars(0, tb_counter_16bit);

        start_clk = 1;
        #100;
        rst = 1;
        #100;
        rst = 0;
        #100;
        rst=1;
        rst=0;
        #100;
        rst=0;
        rst=1;
        #100;
        rst=1;
        #1
        rst=0;
        #100;




        $finish;
    end

endmodule