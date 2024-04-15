
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
    input wire  [31:0] rx,
    output reg COUNT_SIG,
	 input wire rxValid
    );  // BYTE received is valid
	
	 initial begin 
	   COUNT_SIG = 0; 	
	 end 
	 
	 reg [31:0] COMMAND;
	 
	 
	 always @(posedge rxValid) begin
		if (rx==32'hFFFF_FFFF) begin COUNT_SIG <= 1;end
		else if(rx==32'h1111_1111) begin COUNT_SIG <= 0; end
	 end
	 
	 
endmodule