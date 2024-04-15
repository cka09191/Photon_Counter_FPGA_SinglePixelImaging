// SPI Byte Interface, top level module
// Platform: Altera Cyclone IV using Quartus 21.1 (>=16.1)
// Documentation: https://coertvonk.com/hw/math-talk/byte-exchange-with-a-fpga-as-slave-30818
//
// Demonstrates byte exchange with Arduino where FPGA is the SPI slave
//   - The Arduino sends an alternating pattern of 0xAA and 0x55 to the FPGA.
//   - On the FPGA, LED[0] will be on when it receives 0xAA.  Consequentially it will blink with 10% duty cycle.
//   - The FPGA always returns 0x55, what is displayed on the serial port.
//   
// The protocol is specified at https://coertvonk.com/hw/math-talk/bytes-exchange-protocol-30814
//
// GNU GENERAL PUBLIC LICENSE Version 3, check the file LICENSE for more information
// (c) Copyright 2015-2022, Coert Vonk
// All rights reserved.  Use of copyright notice does not imply publication.
// All text above must be included in any redistribution

`timescale 1ns / 1ps
`default_nettype none

// for SPI MODE 3
module usb_test( input wire clk,  
                 input wire [8191:0] rx,
					  output reg [0:0] LED = 0,
					  output reg [8191:0] tx = 0
                  ); // PLL clock  locked
								 
 
	always @(posedge clk)
	   tx<=rx;
			
endmodule
