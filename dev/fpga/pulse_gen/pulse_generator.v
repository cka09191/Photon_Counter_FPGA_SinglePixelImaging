module pulse_generator(
    input wire clk,
    input wire pulse_clk,
    input wire [2:0] cnt,//delay between pulses
    output reg pulse1,
    output reg pulse2
);
wire [7:0] delay = {cnt[2:0],5'b0};
parameter pulse_size = 4;
reg [7:0] counter1=0;
reg [7:0] counter2=0;
reg [7:0] counter3=0;
reg activated = 1'b0;
reg [2:0] pulse_clk_r;  always @(posedge clk) pulse_clk_r <= { pulse_clk_r[1:0], pulse_clk };
wire pulse_clk_rising  = ( pulse_clk_r[2:1] == 2'b01 );

//make 20ns pulse1 when pulse_clk from clk(400Mhz)
//after delay, make 20ns pulse2 when pulse_clk from clk(400Mhz)
always @(posedge clk) begin
    if(pulse2) begin 
        if (counter3 > pulse_size) begin
            counter3 <= 0;
            pulse2 <= 0;
        end
        else begin
            pulse2 <= 1;
            counter3 <= counter3 + 1;
        end
    end
    
    if(pulse1) begin 
        if (counter1 > pulse_size) begin
            counter1 <= 0;
            pulse1 <= 0;
        end
        else
            pulse1 <= 1;
            counter1 <= counter1 + 1;
    end
    if(activated) begin
        counter2 <= counter2 + 1;
        if(counter2 > delay) begin
            pulse2 <= 1;
            counter2 <= 0;
            activated <= 0;
        end
    end
    else if(pulse_clk_rising) begin
        pulse1 <= 1;
        counter1 <= 0;
        activated <= 1;
    end

end
endmodule