import time

import serial


class ArduinoSerialCheckProtocol:
    readnext = '1'.encode('utf-8')
    readbefore = '2'.encode('utf-8')
    readfirst = '4'.encode('utf-8')
    index = '7'.encode('utf-8')
    resetindex = '8'.encode('utf-8')
    total = 'a'.encode('utf-8')
    looploopindex = 'b'.encode('utf-8')
    def __init__(self, port, baudrate, parity=serial.PARITY_NONE, check=0, stopbits=1, timeout=0):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout)
        self.check = check
        # 시리얼포트 접속
        self.ser.isOpen()
        self.check_connection(check)
        self.ser.set_buffer_size(rx_size=12800, tx_size=12800)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.__exit__(exc_type, exc_val, exc_tb)

    def check_connection(self, times=5):
        """
        :param second:
        :return: respond
        """
        i = 0
        while (True):
            self.send(self.index)

            if (i >= times):
                break
            while (self.ser.inWaiting == 0):
                pass
            try:
                data = int(self.ser.readline().decode('utf-8'))
                i += 1
            except Exception:
                pass

            # self.ser.write(bytes("1", 'utf-8'))

            # self.ser.flush()
            #     response = self.ser.readline()
            #     print(response)
            #     response = self.ser.readline()
            #     print(response)
            # power_measurements.append(resint)
        # return np.mean(power_measurements)

    def receive(self):
        try:
            data = int(self.ser.readline().decode())
        except Exception:
            return None
        return data

    def receive_wait(self):
        r = None
        while (r == None):
            r = self.receive()
        return r

    def transaction(self, message):
        if message == self.total:
            return self.receive_whole_voltage()
        r = None
        self.flush()
        while (r == None):
            self.send(message)
            r = self.receive()
        return r
    def receive_whole_voltage(self):
        self.flush()
        self.ser.reset_input_buffer()
        self.send(self.total)
        r = self.ser.readlines()
        for i in range(len(r)):
            r[i] = r[i].decode()
        return r


    def send(self, data):
        try:
            self.ser.write(data)
        except Exception:
            return None
        return data

    def flush(self):
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()


if __name__ == "__main__":
    a = ArduinoSerialCheckProtocol("COM7", 115200, check=0, stopbits=2, parity=serial.PARITY_EVEN)
    time.sleep(5)
    print("checkcomplete")
    for i in range(5):
        a.send(ArduinoSerialCheckProtocol.readfirst)
        print(a.receive_wait())
        a.send('1'.encode('utf-8'))
        print(a.receive_wait())
        print(a.receive_wait())
        a.send(ArduinoSerialCheckProtocol.readfirst)
        print(a.receive_wait())
        a.send('7'.encode('utf-8'))
        a.send(ArduinoSerialCheckProtocol.resetindex)
        print(a.receive_wait())
