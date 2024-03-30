module tb_counter();
  
reg clk;
reg SCLK;
wire RD;
reg DMD_sig;
wire rst;
reg sig;
reg MOSI;
wire MISO;
reg SS;
wire [15:0] rx;
wire [15:0] cnt;
wire [15:0] data_out;
wire rxValid;
reg [7:0] misoData;
reg [7:0] mosiData;

localparam T = 250;   // SPI clock period (4 MHz)
localparam Tsys = 20; // external FPGA clock period (50 MHz)

spi_short_module SPI( .sysClk(clk),  
                      .SCLK(SCLK),        
						          .MOSI(MOSI),        
						          .MISO(MISO),      
						          .SS(SS),         
						          .tx(data_out),    
						          .rx(rx),
						          .rxValid(rxValid)  
						  );

controller controller1(
                      .CLK(clk),
                      .COMMAND(rx),
                      .END_COUNT(rst),
	                    .READ_DATA(RD)
    );

DataMemory Memory1(
  .clk(clk),
  .RD(RD),
  .DMD_sig(DMD_sig),
  .data_in(cnt),
  .data_out(data_out),
  .rxValid(rxValid)
);

counter_16bit count1(
  .clk50Mhz(clk),
  .DMD_sig(DMD_sig),
  .sig(sig),
  .rst(rst),
  .cnt(cnt)
);


initial begin
  clk = 0;
  sig = 0;
  DMD_sig = 0;
end

always 
	   forever 
		   #5 clk = ~clk;
		   

always #10 sig = ~sig;
 

always@(posedge DMD_sig) begin
  $display("%b",data_out);
end

initial begin
  repeat(1000) begin
    #250 DMD_sig =~DMD_sig;
    #10 DMD_sig=~DMD_sig;
  end
  
  //rx = 1;
  SS = 1'b0;  // activate slave-select
  mosiData =  8'h01;
	exchange_byte( mosiData, misoData );
	SS = 1'b1;   // de-activate slave-select
	MOSI = 1'bz;
  
  while(misoData!==2) #1;
  
  //rx = 2;
  while(misoData!==0) begin
  SS = 1'b0;  // activate slave-select
  mosiData =  8'h02;
	exchange_byte( mosiData, misoData );
	SS = 1'b1;   // de-activate slave-select
	MOSI = 1'bz;
  end
  
  //rx = 0;
  SS = 1'b0;  // activate slave-select
  mosiData =  8'h00;
	exchange_byte( mosiData, misoData );
	SS = 1'b1;   // de-activate slave-select
	MOSI = 1'bz;
	
	$finish;
end

task exchange_byte ( input [7:0] mosiData,
								output [7:0] misoData );
		integer jj;
		begin
		  
			for (jj = 0; jj < 16; jj = jj + 1 )
				begin
					#(T/2); SCLK=1'b0; MOSI = mosiData[15 - jj];  // drive on falling edge
					#(T/2); SCLK=1'b1; misoData = { misoData[14:0], MISO };  // sample in rising
				end
		end
	endtask

endmodule







