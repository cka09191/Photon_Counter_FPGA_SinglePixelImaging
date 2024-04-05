"""


@author Gyeongjun Chae(https://github.com/cka09191)
"""
import time
from pyftdi.spi import SpiController
from os import environ
from pyftdi.misc import to_bool

class usb_transaction_module:
    """Basic test for a RFDA2125 Digital Controlled Variable Gain Amplifier
       selected as CS2,
       SPI mode 0
    """

    def __init__(self):
        self._spi = SpiController(cs_count=1)
        self._port = None

    def open(self):
        """Open an SPI connection to a slave"""
        url = environ.get('FTDI_DEVICE', 'ftdi:///1')
        debug = to_bool(environ.get('FTDI_DEBUG', 'off'))
        self._spi.configure(url, debug=debug)
        self._port = self._spi.get_port(2, freq=10E6, mode=0)
    
    def End_Signal(self):
        Data = int(self._port.exchange([0x00,0x01],2))
        return Data

    def Start_Read(self):
        Data = int(self._port.exchange([0x00,0x11],2))
        return Data

    def End_Read(self):
        Data = int(self._port.exchange([0x00,0x00],2))
        return Data

    def close(self):
        """Close the SPI connection"""
        self._spi.terminate()


if __name__ == "__main__":
    usb_fpga_0 = usb_transaction_module()
    usb_fpga_0.open()
    # 1. Start_DMD initialize 
    # 2. END_DMD if DMD 작동 끝나면 시그널 줌
    # 3. Start_Read if fpga로부터 데이터 받는 순간 시그널 줌
    # 4. End_Read if fpga로부터 데이터 0 받는 순간 시그널 줌
    usb_fpga_0.close()

    