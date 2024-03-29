

// SPI Byte Interface, byte interface module
// Platform: Altera Cyclone IV using Quartus 16.1
// Documentation: http://www.coertvonk.com/technology/logic/connecting-fpga-and-arduino-using-spi-13067
// Inspired by: http://fpga4fun.com/SPI2.html
//
// GNU GENERAL PUBLIC LICENSE Version 3, check the file LICENSE for more information
// (c) Copyright 2015-2016, Coert Vonk
// All rights reserved.  Use of copyright notice does not imply publication.
// All text above must be included in any redistribution

/*
basic FPGA SPI module
    sysClk:
		internal FPGA clock
	SCLK:
		SPI clock
	MOSI:
		SPI master out, slave in pin
	MISO:
		SPI slave in, master out pin
	SS:
		SPI slave select pin
		when SS is rising edge, the module is activated
		when SS is falling edge, the module is deactivated
	tx:
		data to transmit
	rx:
		data received
	rxValid:
		data received is valid
 */

`timescale 1ns / 1ps
`default_nettype none

// for SPI MODE 3
module spi_short_module( input wire sysClk,      // internal FPGA clock
                    input wire SCLK,        // SPI clock
						  input wire MOSI,        // SPI master out, slave in
						  output wire MISO,       // SPI slave in, master out
						  input wire SS,          // SPI slave select
						  input wire [15:0] tx,    // BYTE to transmit
						  output wire [15:0] rx   // BYTE received
						  /*output wire rxValid*/ );  // BYTE received is valid

	// Synchronize SCLK to FPGA domain clock using a two-stage shift-register,
	//   where bit [0] takes the hit of timing errors.
	// For SCLK and SS a third stage is used to detect rising/falling
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

	reg [15:0] buffer = 8'dxxxx;

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
	/*assign rxValid = (state == 4'd15) && SCLK_rising;*/ // short received is valid

	reg MISO_r = 1'bx;	
	assign MISO = SS_active ? MISO_r : 1'bz;
	
	always @(posedge sysClk)
		if( SS_active )
			begin
			
				if( SCLK_rising )         // INPUT on rising SPI clock edge
					if( state != 3'd15 ) 
						buffer <= rx;
								
				if( SCLK_falling)         // OUTPUT on falling SPI clock edge
					if ( state == 3'b000 )
						begin 
							MISO_r <= tx[15];    //   start by sending the MSb
							buffer <= tx;       //   remaining bits are send from buffer
						end
					else
						MISO_r <= buffer[15];  //   send next bit

			end
						
endmodule
