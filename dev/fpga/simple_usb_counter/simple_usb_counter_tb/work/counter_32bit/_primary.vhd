library verilog;
use verilog.vl_types.all;
entity counter_32bit is
    port(
        clk50Mhz        : in     vl_logic;
        sig             : in     vl_logic;
        rst             : in     vl_logic;
        cnt             : out    vl_logic_vector(31 downto 0)
    );
end counter_32bit;
