
/*
basic FPGA Controller module in 16bit
    CLK:
        clock signal to synchronize
        at rising edge of CLK, COMMAND signal is valid

    COMMAND:
        signal from master, from SPI module
        0x00: idle(stop counting),
		0x01: start counting
    START_COUNT:
        signal to indicate start of counting

* @author Gyeongjun Chae(https://github.com/cka09191)
 */

module controller(
    input wire CLK,
    input wire [15:0] COMMAND,
    output reg START_COUNT
    );  // BYTE received is valid

    initial begin
        START_COUNT <= 0;
    end

    always @(posedge CLK) begin
        if (COMMAND == 16'h0001) begin
            START_COUNT <= 1;
        end
        else begin
            START_COUNT <= 0;
        end
    end
endmodule