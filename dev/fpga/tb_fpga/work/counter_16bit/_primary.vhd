library verilog;
use verilog.vl_types.all;
entity counter_16bit is
    port(
        clk50Mhz        : in     vl_logic;
        DMD_sig         : in     vl_logic;
        sig             : in     vl_logic;
        rst             : in     vl_logic;
        cnt             : out    vl_logic_vector(15 downto 0)
    );
end counter_16bit;
