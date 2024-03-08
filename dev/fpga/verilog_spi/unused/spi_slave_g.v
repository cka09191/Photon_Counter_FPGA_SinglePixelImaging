
/*
 * basic SPI slave module
 * mode 3, CPOL=1, CPHA=1
 * MSB first
 * com_clk:
    clock signal from master
 * CS:
    chip select signal from master
    1: idle, 0: transaction
 * byte_transaction_signal:
    signal to indicate state of transaction of a byte
    1: transaction, 0: idle
 * MISO_data:
    data to be sent to master
 * MOSI_data: data received from master
    (there is data when byte_transaction_signal is 1)
 * counter:
    counter to 8 bits
 * @author Gyeongjun Chae(https://github.com/cka09191)
 */

module SPI_slave (
    input wire com_clk,
    input wire CS,
    input wire MOSI,
    output reg MISO,
    input wire[7:0] MISO_data,
    output reg[7:0] MOSI_data,
    output reg byte_transaction_signal
);
    reg [2:0] counter;

    always @(negedge CS) begin
        MOSI_data<=8'b00000000;
        counter <= 3'b000;
        byte_transaction_signal <= 0;
    end

    wire clk_when_CS = com_clk & ~CS;
    always @(posedge clk_when_CS) begin
        // when transaction starts
        if (byte_transaction_signal == 0) begin
            byte_transaction_signal <= 1;
        end
        // when transaction ends


        MOSI_data[7-counter] <= MOSI;

        MISO<=MISO_data[counter];

        counter = counter + 1;
        if (counter == 7) begin
            byte_transaction_signal <= 0;
        end
    end

endmodule
