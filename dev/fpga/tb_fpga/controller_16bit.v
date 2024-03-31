
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
    input wire  [15:0] rx,
    output reg END_COUNT,
	 output reg READ_DATA
    );  // BYTE received is valid
	
	 initial begin 
	    END_COUNT = 0;
      READ_DATA = 0; 	 
	 end 
	 
	 reg [1:0] COMMAND;
	 
	 always @(posedge CLK) begin
		case(COMMAND)
				16'b0000_0000_0000_0001:	END_COUNT <= 1; // rx=0 start
				16'b0000_0000_0000_0011:	READ_DATA <= 1; // rx
				16'b0000_0000_0000_0000: READ_DATA <= 0;
		endcase
	 end
	 
	 always @(posedge CLK) begin
		case(rx)
				16'b0000_0000_0000_0001:	COMMAND <= rx; // rx=0 start
				16'b0000_0000_0000_0011:	COMMAND <= rx; // rx
				16'b0000_0000_0000_0000: COMMAND <= rx;
		endcase
	 end
	 
endmodule