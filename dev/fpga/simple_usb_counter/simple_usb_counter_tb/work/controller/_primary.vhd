library verilog;
use verilog.vl_types.all;
entity controller is
    port(
        CLK             : in     vl_logic;
        rx              : in     vl_logic_vector(31 downto 0);
        COUNT_SIG       : out    vl_logic
    );
end controller;
