


module controller(
    input wire CLK,
    input wire COMMAND,
    output wire [7:0] START_COUNT
    );  // BYTE received is valid

    initial begin
        START_COUNT = 0;
    end

    always @(posedge CLK) begin
        if (COMMAND) begin
            START_COUNT = 1;
        end
    end