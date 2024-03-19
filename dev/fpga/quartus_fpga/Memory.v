module DataMemory (
    input wire clk,      // Clock signal
    input wire rst,      // Reset signal
    input wire enable,   // Signal to enable data emission
	 input wire [7:0] data_in,
    output reg [7:0] data_out // Output data
);

// Define memory to store 255 pieces of data
reg [15:0] memory [0:1022];

// Address register to read data from memory
reg [9:0] addr;

// Output register to hold data to emit
reg [15:0] output_data;

// Initialize address register
always @ (posedge clk or posedge rst) begin
    if (rst)
        addr <= 0;
    else if (enable)
        addr <= addr + 1;
end

// Read data from memory based on address
always @ (posedge clk) begin
    if (enable)
        output_data <= memory[addr];
end

// Emit data when enable signal is applied
always @ (posedge clk) begin
    if (enable)
        data_out <= output_data;
    else
        data_out <= 8'b0; // Output zero when enable signal is low
end

// You need to initialize memory with your data
// For example:
// initial begin
//    memory[0] = 8'hAA;
//    memory[1] = 8'hBB;
//    ...
//    memory[254] = 8'hFF;
// end

endmodule
