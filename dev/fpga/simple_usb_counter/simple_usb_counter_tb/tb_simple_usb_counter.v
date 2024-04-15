module tb_counter();
  
reg clk;
reg SCLK;
wire RD;
wire rst;
reg sig;
reg MOSI;
wire MISO;
reg SS;
wire [31:0] rx;
wire [31:0] cnt;
wire [31:0] tx;
reg [31:0] misoData;
reg [31:0] mosiData;

localparam T = 250;   // SPI clock period (4 MHz)
localparam Tsys = 20; // external FPGA clock period (50 MHz)

spi_short_module SPI( .sysClk(clk),  
                      .SCLK(SCLK),        
						          .MOSI(MOSI),        
						          .MISO(MISO),      
						          .SS(SS),         
						          .tx(tx),    
						          .rx(rx) 
						  );

controller controller1(
                      .CLK(clk),
                      .rx(rx),
                      .COUNT_SIG(rst)
    );



counter_32bit count1(
  .clk50Mhz(clk),
  .sig(sig),
  .rst(rst),
  .cnt(tx)
);


initial begin
  clk = 0;
  sig = 0;
end

always 
	   forever 
		   #5 clk = ~clk;
		   

always #10 sig = ~sig;
 

/*always@(posedge clk) begin
  $display("rising:%b, falling:%b, rxValid:%b, state:%d,SS_falling:%b, data_in:%d, COMMAND:%d, addres:%d RD:%b, memory[0]:%d, memory[1]:%d, memory[999]:%d, memory[1000]:%d,rx:%b",
  SPI.SCLK_rising,SPI.SCLK_falling,rxValid, SPI.state,SPI.SS_falling,Memory1.data_in,controller1.COMMAND,Memory1.addr,RD,Memory1.memory[0], Memory1.memory[1], Memory1.memory[999], Memory1.memory[1000],rx);
end
*/

always@(posedge clk) begin
  $display("COUNT_SIG:%b",controller1.COMMAND);
end

initial begin
  SS = 1'b1;
  #100;
  //rx = 1;
  SS = 1'b0;  // activate slave-select
  mosiData =  32'hFFFF_FFFF;
	exchange_byte( mosiData, misoData );
	SS = 1'b1;   // de-activate slave-select
	
	#100000;
	
  SS = 1'b0;  // activate slave-select
  mosiData =  32'h0000_0000;
	exchange_byte( mosiData, misoData );
	SS = 1'b1;   // de-activate slave-select
	
	$finish;
end

task exchange_byte ( input [31:0] mosiData,
								output [31:0] misoData );
		integer jj;
		begin
		  
			for (jj = 0; jj < 32; jj = jj + 1 )
				begin
					#(T/2); SCLK=1'b0; MOSI = mosiData[31 - jj];  // drive on falling edge
					#(T/2); SCLK=1'b1; misoData = { misoData[30:0], MISO };  // sample in rising
				end
		end
	endtask

endmodule








