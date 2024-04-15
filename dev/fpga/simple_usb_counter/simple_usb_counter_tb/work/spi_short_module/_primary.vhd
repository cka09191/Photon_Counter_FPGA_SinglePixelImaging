library verilog;
use verilog.vl_types.all;
entity spi_short_module is
    port(
        sysClk          : in     vl_logic;
        SCLK            : in     vl_logic;
        MOSI            : in     vl_logic;
        MISO            : out    vl_logic;
        SS              : in     vl_logic;
        tx              : in     vl_logic_vector(31 downto 0);
        rx              : out    vl_logic_vector(31 downto 0)
    );
end spi_short_module;
