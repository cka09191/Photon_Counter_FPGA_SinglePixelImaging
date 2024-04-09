library verilog;
use verilog.vl_types.all;
entity controller is
    port(
        CLK             : in     vl_logic;
        rx              : in     vl_logic_vector(15 downto 0);
        END_COUNT       : out    vl_logic;
        READ_DATA       : out    vl_logic
    );
end controller;
