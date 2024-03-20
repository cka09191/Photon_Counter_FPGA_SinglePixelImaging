

"""
This module contains functions for running an experiment with a DMD controller and Arduino.

Functions:
- _hadamard_image_data(pixel, size_im, reversed=False): Generate Hadamard image data.
- voltage_read(arduino, start, end): Read voltage from Arduino.
- experiment(pixel, picturetime, file, im_size=150, seq_length=64): Run the experiment.

@author Gyeongjun Chae(https://github.com/cka09191)
"""


import os
import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.linalg import hadamard

from ALP4 import tAlpDynSynchOutGate, ALP_DEV_DYN_SYNCH_OUT1_GATE
from arduino_transaction_module import arduino_transaction_module
from dmd_controller import dmd_controller


def _hadamard_image_data(_pixel: int, size_im: int, _reversed=False):
    """
    Generate Hadamard image as a numpy array.

    Args:
        pixel (int): Number of pixels.
        size_im (int): Size of the image.
        reversed (bool, optional): Whether to reverse the Hadamard pattern. Defaults to False.

    Returns:
        numpy.ndarray: Hadamard image data.
    """
    _ = 1
    if _reversed is True:
        _ = -1
    hadamard_array = np.array(hadamard(_pixel),np.int8) * _
    pixel_sqrt_is_length = int(np.sqrt(_pixel))
    image_data = dmd_controller.array_set_to_imagedata(hadamard_array, pixel_sqrt_is_length, size_im=size_im)
    return np.array(image_data)


def voltage_read(arduino: arduino_transaction_module):
    """
    Read voltage data and return as a numpy array.

    Args:
        arduino (ArduinoSerialCheckProtocol): Arduino protocol object.
        start (int): Start index.
        end (int): End index.

    Returns:
        numpy.ndarray: Voltage data.
    """
    return np.array(arduino.transaction(arduino.total), dtype=np.int32)


def experiment(_pixel: int, _picture_time: int, _name_file: str, _size_im=150, _length_seq=64):
    """
    Run the experiment.

    Args:
        _pixel (int): Number of pixels.
        _picture_time (int): Time for each picture.
        _file_name (str): File to save the data.
        _size_im (int, optional): Size of the image. Defaults to 150.
        _length_seq (int, optional): Length of the sequence. Defaults to 64.
    """

    print('DMD initializing', end='')
    dmd = dmd_controller()
    gate = tAlpDynSynchOutGate()
    gate.Period = 1
    gate.Polarity =0
    gate.Gate[0] = 1
    dmd.dmd.DevControlEx(ALP_DEV_DYN_SYNCH_OUT1_GATE, gate)
    print('...done')

    print('arduino initializing', end='')
    arduino_protocol = arduino_transaction_module("COM7", 115200, 'E', 5, 2, 1)
    arduino_protocol.flush()
    print('...done')

    print('Pattern and key generating', end='')
    print(f"pixel:{_pixel}, picturetime:{_picture_time}, im_size:{_size_im}")
    start_time = time.perf_counter()
    length_pattern = int(np.sqrt(_pixel))

    # hadamard_image_data_set is a set of hadamard images in two polarities
    hadamard_image_data_set = np.zeros((_pixel*2, 768, 1024),np.uint8)
    hadamard_image_data_set[0::2,:,:] = _hadamard_image_data(_pixel, _size_im)
    hadamard_image_data_set[1::2,:,:] = _hadamard_image_data(_pixel, _size_im, True)
    
    # key is inverse of hadamard_array which is used to decode the image
    hadamard_array = np.array(hadamard(_pixel))
    key = np.linalg.inv(hadamard_array.reshape(_pixel, _pixel))
    print('...done')
    print(f"processing time:{time.perf_counter() - start_time}")

    print('uploading', end='')
    start_time = time.perf_counter()
    slides = dmd.upload(hadamard_image_data_set, hadamard_image_data_set.shape[0], 1, _length_seq)
    print('...done')
    print(f"uploading time:{time.perf_counter() - start_time}")

    
    print('experiment and aquisition start', end='')
    total_data = np.array([])

    # start_time is used to measure the time for the whole aquisition and communication
    start_time = time.perf_counter()
    # measure_time_total is the time for each measurement of the sequence
    measure_time_total = []
    for slide in slides:
        length_acquired_data_arduino = 0
        _length_seq_now = _length_seq

        # if the last slide is not a full sequence, the length of the sequence is changed
        if int(slide == slides[-1]):#??
            _length_seq_now = (_pixel * 2) % _length_seq

        # repeat until the length of the acquired data is the same as the length of the sequence
        while (length_acquired_data_arduino != _length_seq_now):
            arduino_protocol.send(arduino_transaction_module.resetindex)
            measure_start_time = time.perf_counter()
            dmd.slideshow(_picture_time, slide, False)
            dmd.wait()
            measure_time_total.append( time.perf_counter() - measure_start_time)
            arduino_protocol.flush()
            length_acquired_data_arduino = arduino_protocol.transaction(arduino_transaction_module.index)
            print(f'length_acquired_data_arduino:{length_acquired_data_arduino}, _length_seq_now:{_length_seq_now} ')

        arduino_protocol.send(arduino_transaction_module.readfirst)
        total_data = np.append(total_data, voltage_read(arduino_protocol))
        print('.', end='')

    print('done')
    print('total aquisition time: ', np.sum(measure_time_total))
    print('total aquisition and communication time: ', time.perf_counter() - start_time)

    # measure is the difference between two patterns in opposite polarities of hadamard pattern
    measure = total_data[0::2] - total_data[1::2]
    print(measure.shape)
    print(measure)
    print(length_pattern)
    time.sleep(100)
    
    plt.imshow(measure.reshape((length_pattern, length_pattern)))
    plt.show()
    plt.pause(0.1)
    imarr = np.matmul(key, measure)
    im = imarr
    plt.imshow(np.transpose(im.reshape((length_pattern, length_pattern))))
    plt.show()
    plt.pause(0.1)

    print('experiment and aquisition end, disconnect Arduino and DMD', end='')
    arduino_protocol.__exit__()
    dmd.__exit__()
    print('...done')

    print('saving data', end='')
    start_time = time.perf_counter()
    np.save(_name_file, total_data.reshape((_pixel, 2)))
    print('...done')
    print(f"saving time:{time.perf_counter() - start_time}")



# Example usage
if __name__ == '__main__':
    DIRECTORY = 'C:\\Users\\CHAEGYEONGJUN\\iCloudDrive\\Desktop\\test\\new0204n\\'
    FILENAME = 'test'
    PIXEL = [256]
    PICTURETIME = [10000]
    os.makedirs(DIRECTORY, exist_ok=True)

    explist = [[DIRECTORY + f"{FILENAME}_{pixel}_{rptime}", pixel, rptime] for rptime in PICTURETIME for pixel in PIXEL]
    for (FILENAME, pixel, picturetime) in explist:
        experiment(pixel, picturetime, FILENAME, _length_seq=768, _size_im=300)
