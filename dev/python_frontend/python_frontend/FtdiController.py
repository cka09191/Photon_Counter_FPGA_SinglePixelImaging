from pyftdi.spi import SpiController

class FtdiController:
    def __init__(self, cs_count = 2, freq = 1e6, mode = 0, cs = 1):
        self.spi = SpiController(cs_count=cs_count)
        self.spi.configure('ftdi://ftdi:232h/1')
        self.port = self.spi.get_port(1, freq=1e6, mode=0)
    
    def write(self, data, length):
        data = self.port.exchange(data, length)
        return data
