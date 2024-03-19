phony:
	make help

help:## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

wave:## Run timing test must specify uut
	@echo "Running timing test"
	@iverilog -o test ./dev/fpga/verilog_spi/tb_$(uut)  ./dev/fpga/verilog_spi/$(uut)
	@echo "Running vvp"
	@vvp test
	@gtkwave `grep -oE '\$dumpfile\(\".+?\"\)' ./dev/fpga/verilog_spi/tb_$(uut) | sed 's/\$dumpfile(\"//g' | sed 's/")//g'`
