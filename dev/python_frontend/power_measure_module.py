# Todo: calculate wavelength with responsitivity
#
import time

import numpy as np

from arduino_transaction_module import arduino_transaction_module



class power_measure_module:
    def __init__(self, protocol: arduino_transaction_module):
        self.protocol = protocol

    def mean(self, second=2, reps=10):
        """
        :param second: 총 측정 시간
        :param reps: 측정 횟수
        :param wavelength: 파장
        :return: 평균값
        """

        power_measurements = []
        sleeptime = second/(reps-1)

        power_measurements.append(self.measure())
        for i in range(reps-1):
            time.sleep(sleeptime)
            power_measurements.append(self.measure())

        return np.mean(power_measurements)

    def measure(self):
        while (True):
            meas = self.protocol.receive()
            if meas is not None:
                return meas

    def flush(self):
        self.protocol.flush()


if __name__ == "__main__":
    arduinoprotocol = arduino_transaction_module("COM7", 115200, 'E', 5, 2, 1)
    powermeter = power_measure_module(arduinoprotocol)
    timestart = time.time()
    print(powermeter.mean(second = 3,reps=40))
    print(f"경과시간{time.time() - timestart}")
    # 10.35초

    # timestart = time.time()
    # for a in range(100000):
    #     powermeter.measure()
    # print(f"경과시간{time.time() - timestart}")

    # timestart = time.time()
    # print(f"", powermeter.mean(second=0, reps=100000))
    # print(f"경과시간{time.time() - timestart}")
    # 29초: 초당 약 3398회 측정가능한 것으로 계산, 주로 통신 속도때문일 것으로 생각됨

