`timescale 1ns / 1ps
`default_nettype none

module SPI(
	input wire sysClk,
	input wire SCLK,
	input wire MOSI,
	output wire	MISO,
	input wire SS,
	input wire [15:0] tx,
	output wire [15:0] rx
);

reg [2:0] SCLK_r;  always @(posedge sysClk) SCLK_r <= { SCLK_r[1:0], SCLK };
	reg [2:0] SS_r;    always @(posedge sysClk) SS_r   <= {   SS_r[1:0],   SS };
	reg [1:0] MOSI_r;  always @(posedge sysClk) MOSI_r <= {   MOSI_r[0], MOSI };
	wire SCLK_rising  = ( SCLK_r[2:1] == 2'b01 );
	wire SCLK_falling = ( SCLK_r[2:1] == 2'b10 );
	wire SS_falling   = ( SS_r[2:1] == 2'b10 );
	wire SS_active    = ~SS_r[1];   // synchronous version of ~SS input
	wire MOSI_sync    = MOSI_r[1];  // synchronous version of MOSI input

	// circular buffer, initialized with data to be transmitted	
	// - on SCLK_falling, bit [15] is transmitted by through MISO_r
	// - on SCLK_rising, MOSI_sync is shifted in as bit [0]
	// see http://www.coertvonk.com/technology/logic/connecting-fpga-and-arduino-using-spi-13067/3#operation

	reg [15:0] buffer = 15'bxxxxxxxx;

	// current state logic

	reg [3:0] state = 4'bxxxx; // state corresponds to bit count
	
	always @(posedge sysClk)
		if ( SS_active )
			begin
				if ( SS_falling )   // start of 1st byte
					state <= 3'd0;
				if ( SCLK_rising )  // input bit available
					state <= state + 3'd1;
			end

	// input/output logic
	
	assign rx      = {buffer[14:0], MOSI_sync};       // bits received so far

	reg MISO_r = 1'bx;	
	assign MISO = SS_active ? MISO_r : 1'bz;
	
	always @(posedge sysClk)
		if( SS_active )
			begin
			
				if( SCLK_rising )         // INPUT on rising SPI clock edge
					if( state != 4'b1111 ) 
						buffer <= rx;
								
				if( SCLK_falling)         // OUTPUT on falling SPI clock edge
					if ( state == 4'b000 )
						begin 
							MISO_r <= tx[15];    //   start by sending the MSb
							buffer <= tx;       //   remaining bits are send from buffer
						end
					else
						MISO_r <= buffer[15];  //   send next bit

			end
						
endmodule