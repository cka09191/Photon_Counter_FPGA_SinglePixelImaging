
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
    input wire  [15:0] COMMAND,
    output reg START_COUNT,
	 output reg READ_DATA
    );  // BYTE received is valid

    initial begin
        START_COUNT <= 0;
    end

    always @(negedge CLK) begin
        if (COMMAND == 16'hFFFF) begin
            START_COUNT <= 1;
        end
        else if(COMMAND == 16'h0000) begin
            START_COUNT <= 0;
        end
        else if (COMMAND[15:4] == 16'hFFF ) begin
            START_COUNT <= 1;
        end
        else if (COMMAND[15:8] == 16'hFF & COMMAND[3:0]==16'hF) begin
            START_COUNT <= 1;
        end
        else if (COMMAND[15:12] == 16'hF & COMMAND[7:0]==16'hFF) begin
            START_COUNT <= 1;
        end
        else if (COMMAND[11:0]==16'hFFF) begin
            START_COUNT <= 1;
        end
        else if (COMMAND[15:4]==16'h000) begin
            START_COUNT <= 0;
        end
        else if (COMMAND[15:8]==16'h00 & COMMAND[3:0]==16'h0) begin
            START_COUNT <= 0;
        end
        else if (COMMAND[15:12]==16'h0 & COMMAND[7:0]==16'h00) begin
            START_COUNT <= 0;
        end
        else if (COMMAND[11:0]==16'h000) begin
            START_COUNT <= 0;
        end
        
    end
endmodule