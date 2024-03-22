
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
    input wire DMD_Signal,
    output reg START_COUNT
    );  // BYTE received is valid
	
	reg [2:0] DMD_Signal_r;  always @(posedge sysClk) DMD_Signal_r <= { DMD_Signal_r[1:0], DMD_Siganl };
	wire DMD_Signal_rising  = ( DMD_Signal_r[2:1] == 2'b01 );
	wire DMD_Siganl_falling = ( DMD_Siganl_r[2:1] == 2'b10 );

    initial begin
        START_COUNT <= 0;
    end

    always @(posedge CLK) begin
        if (DMD_Signal_rising) begin
            START_COUNT <= 0;
        else begin
            START_COUNT <= 1;
        end
        
    end
endmodule