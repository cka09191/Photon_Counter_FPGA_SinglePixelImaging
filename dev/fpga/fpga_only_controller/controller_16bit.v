
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
    output reg END_COUNT,
	 output reg READ_DATA
    );  // BYTE received is valid
	
	 
	 always @(posedge CLK) begin
		case(COMMAND)
				1'd0:	END_COUNT <= 1; // rx=0 start
				1'd1:	READ_DATA <= 1; // rx
				1'd2: READ_DATA <= 0;
		endcase
	 end
	 
endmodule