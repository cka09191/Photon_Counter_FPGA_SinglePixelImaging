// Time to Digital Converter
// author: Gyeongjun Chae, San Kim
//
// clk : 500MHz
// Start[0]: pulse1 arrived at 0
// Start[1]: pulse2 arrived at 0
// End[0]: pulse1 arrived after INTERVAL
// End[1]: pulse2 arrived after INTERVAL
// data_arrived : 1 if data is arrived, it continues 2 clock cycles(4ns)
// INTERVAL : time between Start and End, 1 clock cycle is 2ns, at most 256ns(128 clock cycles)
//
// ex: pulse 1, 2 exactly arrived at 0ns, and after 10ns, pulse 1 arrived,
// at 0ns, data_arrived is 1, and 0 at 4ns
// at 0ns, INTERVAL is 0
// at 0ns, START_signal is 00, and END_signal is 11(if there was pulse short before, it will be neglected)
// then,
// at 14ns, data_arrived is 1 at 10ns, and 0,
// at 14ns, INTERVAL is 10 at 10ns
// at 14ns, START_signal is 11, and END_signal is 01, at 10ns
//
// after 128ns, counting will not be continued
module TDC(
	input wire clk,
	input wire pulse1,
	input wire pulse2,
	output reg [1:0] START_signal,
	output reg [1:0] END_signal,
	output reg [5:0] INTERVAL,
	output reg data_arrived
);


reg [5:0] count;
reg notedge_pulse;
wire pulse = pulse1 | pulse2;

initial
begin
	count = 0;
	START_signal <= 2'b00;
	END_signal <= 2'b00;
	notedge_pulse = 0;
	INTERVAL = 0;
	data_arrived = 0;
end


always @(posedge clk) begin
	if(pulse) begin
		if (~notedge_pulse) begin
			if (pulse1 && pulse2) begin
				INTERVAL <= 0;
				data_arrived <= 1;
				START_signal <= 2'b00;
				END_signal <= 2'b11;
				data_arrived <= 1;
			end
			else begin
				if(count == 6'd63) begin
					count <= 0;
					END_signal <= {pulse1, pulse2};
				end
				else begin
					INTERVAL<=count;
					count <= 0;
					START_signal<=END_signal;
					END_signal <= {pulse1, pulse2};
					data_arrived <= 1;
				end
			end
			notedge_pulse <= 1;
		end
		count <= 0;
	end
	else begin
		notedge_pulse <= 0;
		case(count)
			6'd2: begin
				data_arrived <= 0;
				count <= count + 1;
			end
			6'd63: begin
				count <= count;
			end
			default: begin
				count <= count + 1;
			end
		endcase
	end
end


endmodule

