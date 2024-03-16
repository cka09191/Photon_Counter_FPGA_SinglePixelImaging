import multiprocessing
import os
import time

import numpy as np
from matplotlib import pyplot as plt

from ALP4 import tAlpDynSynchOutGate, ALP_DEV_DYN_SYNCH_OUT1_GATE, ALP_LEVEL_HIGH
from ArduinoSerialCheckProtocol import ArduinoSerialCheckProtocol
from DMD_controller import DMD_controller
from PowerMeterWithArduinoSerial import PowerMeterWithArduinoSerial
from scipy.linalg import hadamard


def hadamard_remastered_image_data(pixel: int, size_im: int, reversed=False):
    directory = 'C:\\Users\\CHAEGYEONGJUN\\iCloudDrive\\Desktop\\Test\\hadamard_remaster\\'
    os.makedirs(directory, exist_ok=True)
    filename = f'{pixel}{size_im}.npy'
    if filename in os.listdir(directory):
        return np.load(directory + filename)
    else:
        _ = 1
        if reversed == True:
            _ = -1
        hadamard_array = np.array(hadamard(pixel))
        hadamard_array[0, pixel // 2:0] = -1
        hadamard_array *= _
        pixel_sqrt_is_length = int(np.sqrt(pixel))
        print(hadamard_array)
        imgData = DMD_controller.array_set_to_imagedata(hadamard_array, pixel_sqrt_is_length, size_im=size_im)
        # np.save(directory + filename, imgData)
        return np.array(imgData)


def hadamard_image_data(pixel: int, size_im: int, reversed=False):
    directory = f'C:\\Users\\CHAEGYEONGJUN\\iCloudDrive\\Desktop\\Test\\hadamard_original\\'
    os.makedirs(directory, exist_ok=True)
    filename = f'{pixel}{size_im}_{reversed}.npy'
    if filename in os.listdir(directory):
        return np.load(directory + filename)
    else:
        _ = 1
        if reversed == True:
            _ = -1
        hadamard_array = np.array(hadamard(pixel),np.int8) * _
        pixel_sqrt_is_length = int(np.sqrt(pixel))
        imgData = DMD_controller.array_set_to_imagedata(hadamard_array, pixel_sqrt_is_length, size_im=size_im)
        # np.save(directory + filename, imgData)
        return np.array(imgData)


def voltage_read(arduino: ArduinoSerialCheckProtocol, start: int, end: int):
    datalist = []

    # for i in range(start,end):
    #     voltage = arduino.transaction(arduino.readnext)
    #     datalist.append([voltage, i])
    return np.array(arduino.transaction(arduino.total), dtype=np.int32)


def experiment(pixel: int, picturetime: int, file: str, im_size=150, seq_length=64):
    DMD = DMD_controller()
    Gate = tAlpDynSynchOutGate()
    Gate.Period = 1
    Gate.Polarity =0
    Gate.Gate[0] = 1
    DMD.DMD.DevControlEx(ALP_DEV_DYN_SYNCH_OUT1_GATE, Gate)
    start_time = time.perf_counter()
    length_pattern = int(np.sqrt(pixel))
    hadamard_image_data_set = np.zeros((pixel*2, 768, 1024),np.uint8)
    hadamard_image_data_set[0::2,:,:] = hadamard_image_data(pixel, im_size)
    hadamard_image_data_set[1::2,:,:] = hadamard_image_data(pixel, im_size, True)
    # hadamard_image_data_set = hadamard_image_data(pixel, im_size)

    # dot_size = (length_pattern//2)
    #
    # arrayset = [[0] * x + ([1]*dot_size + [0]*(length_pattern-dot_size))*dot_size+[0]*(pixel - x -dot_size*length_pattern) for x in range(pixel)]
    # hadamard_image_data_set = DMD.array_set_to_imagedata(
    #     arrayset, length_pattern, 150)

    # hadamard_image_data_set = DMD.array_set_to_imagedata(
    #          arrayset, length_pattern, 150)
    # arrayset = [np.array(hadamard(pixel))==1, np.array(hadamard(pixel))==-1]
    # arrayset[0::2, 0] = -1
    # arrayset[0, 0::2] = -1
    hadamard_array = np.array(hadamard(pixel))
    key = np.linalg.inv(hadamard_array.reshape(pixel, pixel))
    print(f"image processing time:{time.perf_counter() - start_time}")
    print(f"image shape:{hadamard_image_data_set[0].shape}")

    start_time = time.perf_counter()
    slides = DMD.upload(hadamard_image_data_set, hadamard_image_data_set.shape[0], 1, seq_length)
    print(f"uploading time:{time.perf_counter() - start_time}")
    while (True):
        arduino_protocol = ArduinoSerialCheckProtocol("COM7", 500000, 'E', 5, 2, 1)
        picturetime = int(input("timing(us)"))
        total = np.array([])
        for st in ['calibrating']:
            if (st == 'calibrating'):
                key = np.linalg.inv(hadamard_array.reshape(pixel, pixel))
                print('calibrating')
            start_time = time.perf_counter()
            arduino_protocol.flush()
            total=np.array([])
            measure_time_total = []
            for slide in slides:
                index = 0
                _seq_length = seq_length
                if int(slide == slides[-1]):
                    _seq_length = (pixel * 2) % seq_length
                while (index != _seq_length):
                    arduino_protocol.send(ArduinoSerialCheckProtocol.resetindex)
                    measure_start_time = time.perf_counter()
                    DMD.slideshow(picturetime, slide, False)
                    DMD.wait()
                    measure_time_total.append( time.perf_counter() - measure_start_time)
                    arduino_protocol.flush()
                    index = arduino_protocol.transaction(ArduinoSerialCheckProtocol.index)
                    end = slide.value * _seq_length
                    start = end - _seq_length
                arduino_protocol.send(ArduinoSerialCheckProtocol.readfirst)
                total = np.append(total, voltage_read(arduino_protocol, start, end))

            print('measure time: ', np.sum(measure_time_total))
            print('total imaging time: ', time.perf_counter() - start_time)
            measure = total[0::2] - total[1::2]
            plt.imshow(measure.reshape((length_pattern, length_pattern)))
            plt.show()
            plt.pause(0.1)
            imarr = np.matmul(key, measure)
            im = imarr
            plt.imshow(np.transpose(im.reshape((length_pattern, length_pattern))))
            plt.show()
            plt.pause(0.1)
            if (st == 'calibrating'):
                hadamard_array_calibration = np.matmul((key), (np.identity(pixel) * im))
                try:
                    key = np.linalg.inv(hadamard_array_calibration.reshape(pixel, pixel))
                except:
                    print('please calibrate again')
                    break
        arduino_protocol.__exit__()

    np.save(file, total.reshape((pixel, 2)))
    DMD.__exit__()






def experiment2(pixel: int, picturetime: int, file: str, im_size=150, seq_length=64):
    arduino_protocol = ArduinoSerialCheckProtocol("COM7", 115200, 'E', 5, 2, 1)
    DMD = DMD_controller()

    start_time = time.perf_counter()
    length_pattern = int(np.sqrt(pixel))
    # hadamard_image_data_set = np.concatenate((hadamard_image_data(pixel, im_size),hadamard_image_data(pixel, im_size,True)))

    # hadamard_image_data_set = hadamard_image_data(pixel, im_size)
    def one_pattern_measure(array=None, pattern_size=2):
        if array is None:
            array = [0, 0, 0, 0]
        index = 0
        while (index != 2):
            arduino_protocol.send(ArduinoSerialCheckProtocol.resetindex)
            DMD.simpletest(array=array, pic=picturetime, pattern_size=pattern_size, size_im=im_size, repeat=False)
            DMD.wait()
            arduino_protocol.flush()
            index = arduino_protocol.transaction(ArduinoSerialCheckProtocol.index)
        arduino_protocol.send(ArduinoSerialCheckProtocol.readfirst)
        return arduino_protocol.transaction(ArduinoSerialCheckProtocol.readnext)

    zero_light = one_pattern_measure([0, 0, 0, 0])
    full_light = one_pattern_measure([1, 1, 1, 1])

    hadamard_image_data_set = hadamard_image_data(pixel, im_size, False)

    # dot_size = (length_pattern//2)
    #
    # arrayset = [[0] * x + ([1]*dot_size + [0]*(length_pattern-dot_size))*dot_size+[0]*(pixel - x -dot_size*length_pattern) for x in range(pixel)]
    # hadamard_image_data_set = DMD.array_set_to_imagedata(
    #     arrayset, length_pattern, 150)

    # hadamard_image_data_set = DMD.array_set_to_imagedata(
    #          arrayset, length_pattern, 150)

    print(f"image processing time:{time.perf_counter() - start_time}")
    print(f"image shape:{hadamard_image_data_set[0].shape}")

    start_time = time.perf_counter()
    slides = DMD.upload(hadamard_image_data_set, hadamard_image_data_set.shape[0], 1, seq_length)
    print(f"uploading time:{time.perf_counter() - start_time}")
    while (True):
        total = np.array([])
        for st in ['calibrating', 'measuring']:
            print(f'status: ready {st}')
            total = np.array([])
            start_time = time.perf_counter()
            arduino_protocol.flush()
            measure_time_total = []
            for slide in slides:

                measure_start_time = time.perf_counter()
                index = 0
                _seq_length = seq_length
                if int(slide == slides[-1]):
                    _seq_length = (pixel) % seq_length
                while (index != _seq_length):
                    arduino_protocol.send(ArduinoSerialCheckProtocol.resetindex)
                    DMD.slideshow(picturetime, slide, False)
                    DMD.wait()
                    measure_time_total.append( time.perf_counter() - measure_start_time)
                    arduino_protocol.flush()
                    index = arduino_protocol.transaction(ArduinoSerialCheckProtocol.index)
                    end = slide.value * _seq_length
                    start = end - _seq_length
                arduino_protocol.send(ArduinoSerialCheckProtocol.readfirst)
                total = np.append(total, voltage_read(arduino_protocol, start, end))
            measure = total[0:pixel]
            if (st == 'calibrating'):
                hadamard_cal = hadamard(pixel) == 1
                key_cal = np.linalg.inv(hadamard_cal.reshape(pixel, pixel))
                arrayset = np.matmul(np.array(key_cal), measure)
                arrayset[arrayset==0]=0.01
                arrayset[arrayset==0]/arrayset.mean()
                hadamard_array_calibration = np.matmul((hadamard_cal), (np.identity(pixel) * arrayset))
                print(hadamard_array_calibration)
                try:
                    key = np.linalg.inv(hadamard_array_calibration.reshape(pixel, pixel))
                except:
                    print('please calibrate again')
                    break

                plt.imshow(arrayset.reshape((length_pattern, length_pattern)))
                plt.show()
                plt.pause(0.1)

        imarr = np.matmul(key, measure)
        im = (imarr)
        plt.imshow(np.flipud(np.transpose(im.reshape((length_pattern, length_pattern)))))
        plt.show()
        plt.pause(0.1)
    np.save(file, total.reshape((pixel, 2)))
    DMD.__exit__()


if __name__ == '__main__':
    directory = 'C:\\Users\\CHAEGYEONGJUN\\iCloudDrive\\Desktop\\test\\new0204n\\'
    filename = 'notfiber'
    os.makedirs(directory, exist_ok=True)
    explist = [[directory + f"{filename}_{pixel}_{rptime}", pixel, rptime] for rptime in [10000] for pixel in [256]]
    for (filename, pixel, picturetime) in explist:
        start_time = time.time_ns()
        experiment(pixel, picturetime, filename, seq_length=768, im_size=300)
