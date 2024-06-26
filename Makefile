CC = gcc
phony:
	@make help

help:## Show this help. if windows: findstr else mac: grep
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


	

wave:## Run timing test must specify uut
	@echo "Running timing test"
	@iverilog -o test ./dev/fpga/verilog_spi/tb_$(uut)  ./dev/fpga/verilog_spi/$(uut)
	@echo "Running vvp"
	@vvp test
	@gtkwave `grep -oE '\$dumpfile\(\".+?\"\)' ./dev/fpga/verilog_spi/tb_$(uut) | sed 's/\$dumpfile(\"//g' | sed 's/")//g'`


wave_ccu:## Run timing test must specify uut
	@echo "Running timing test"
	@iverilog -o test ./dev/fpga/rough_Time_Corelation_Analizer/tb_$(uut)  ./dev/fpga/rough_Time_Corelation_Analizer/$(uut)
	@echo "Running vvp"
	@vvp test
	@gtkwave `grep -oE '\$dumpfile\(\".+?\"\)' ./dev/fpga/rough_Time_Corelation_Analizer/tb_$(uut) | sed 's/\$dumpfile(\"//g' | sed 's/")//g'`

wave_ccu2:## Run timing test must specify uut
	@echo "Running timing test"
	@iverilog -o test ./dev/fpga/rough_Time_Corelation_Analizer/$(uut) ./dev/fpga/rough_Time_Corelation_Analizer/$(uut2) ./dev/fpga/rough_Time_Corelation_Analizer/$(uut3) ./dev/fpga/rough_Time_Corelation_Analizer/$(uut4) ./dev/fpga/rough_Time_Corelation_Analizer/$(uut5)  ./dev/fpga/rough_Time_Corelation_Analizer/$(uut1)
	@echo "Running vvp"
	@vvp test
	@gtkwave `grep -oE '\$dumpfile\(\".+?\"\)' ./dev/fpga/rough_Time_Corelation_Analizer/tb_$(uut) | sed 's/\$dumpfile(\"//g' | sed 's/")//g'`
