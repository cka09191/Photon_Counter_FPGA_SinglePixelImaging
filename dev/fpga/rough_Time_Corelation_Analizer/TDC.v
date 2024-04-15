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
	output reg [6:0] INTERVAL,
	output reg data_arrived
);


reg [6:0] count;
reg data_arrived_internal;
wire pulse = pulse1 | pulse2;

initial
begin
	count = 0;
	START_signal <= 2'b00;
	END_signal <= 2'b00;
	INTERVAL = 0;
	data_arrived = 0;
	data_arrived_internal=0;
end

always @(posedge pulse) begin
	if(pulse1 && pulse2) begin
		data_arrived_internal <= 1;
		INTERVAL <= 0;
		START_signal <= 2'b00;
		END_signal <= 2'b11;
	end
	else begin
		if(count == 7'd127) begin
			END_signal <= {pulse1, pulse2};		
		end
		else begin
			data_arrived_internal = 1;
			INTERVAL<=count;
			START_signal<=END_signal;
			END_signal <= {pulse1, pulse2};
		end
	end
end

always @(posedge clk) begin
	if (~data_arrived_internal) count<=0;
	case(count)
		7'd2: begin
			data_arrived <= 0;
			count <= count + 1;
		end
		default: count <= count + 1;
	endcase
end


endmodule

