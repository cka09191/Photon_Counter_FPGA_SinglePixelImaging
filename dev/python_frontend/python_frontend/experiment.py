

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
import pickle

from ALP4 import tAlpDynSynchOutGate, ALP_DEV_DYN_SYNCH_OUT1_GATE
from python_frontend.arduino_transaction_module import arduino_transaction_module
from python_frontend.controller_dmd import controller_dmd

image_data = {}

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

    if _pixel*_ not in image_data:
        hadamard_array = hadamard(_pixel)*_
        pixel_sqrt_is_length = int(np.sqrt(_pixel))
        image_data[_pixel*_] = controller_dmd.array_set_to_imagedata(hadamard_array, pixel_sqrt_is_length, size_im=size_im)
    return np.array(image_data[_pixel*_])
    


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
    times = {}
    dmd = controller_dmd()
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
    processing_time = time.perf_counter() - start_time
    print(f"processing time:{processing_time}")
    times['processing'] = processing_time


    print('uploading', end='')
    start_time = time.perf_counter()
    slides = dmd.upload(hadamard_image_data_set, hadamard_image_data_set.shape[0], 1, _length_seq)
    print('...done')
    upload_time = time.perf_counter() - start_time
    print(f"uploading time:{upload_time}")
    times['uploading'] = upload_time

    
    print('experiment and aquisition start', end='')
    total_data = np.array([])

    # start_time is used to measure the time for the whole aquisition and communication
    start_time = time.perf_counter()
    # measure_time_total is the time for each measurement of the sequence
    list_measure_time = []
    list_communication_time = []
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
            list_measure_time.append( time.perf_counter() - measure_start_time)
            comm_start_time = time.perf_counter()
            arduino_protocol.flush()
            length_acquired_data_arduino = arduino_protocol.transaction(arduino_transaction_module.index)
            list_communication_time.append(time.perf_counter() - comm_start_time)
            print(f'length_acquired_data_arduino:{length_acquired_data_arduino}, _length_seq_now:{_length_seq_now} ')

        arduino_protocol.send(arduino_transaction_module.readfirst)
        total_data = np.append(total_data, voltage_read(arduino_protocol))
        print('.', end='')

    print('done')
    
    print('total aquisition time: ', np.sum(list_measure_time))
    print('total aquisition and communication time: ', time.perf_counter() - start_time)
    # measure is the difference between two patterns in opposite polarities of hadamard pattern
    measure = total_data[0::2] - total_data[1::2]
    print(measure.shape)
    print(measure)
    print(length_pattern)
    if _name_file == None:
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
    if _name_file is not None:
        if os.path.exists(_name_file):
            os.remove(_name_file)
        print(f"file:{_name_file}")
        print('saving data', end='')
        start_time = time.perf_counter()
        np.save(_name_file, total_data)
        pickle_time_location =str(_name_file)+"_exp"
        #make file
        times['measure_time'] = list_measure_time
        times['communication_time'] = list_communication_time
        with open(pickle_time_location, 'xb') as f:
            pickle.dump(times, f)
        print('...done')
        print(f"saving time:{time.perf_counter() - start_time}")
    else:
        return total_data


def display_exp_data_file(_name_file: str):
    """
    Display the data from the experiment.

    Args:
        _name_file (str): File to load the data.
    """
    data = np.load(_name_file)
    display_exp_data(data)

def display_exp_data(data):
    """
    Display the data from the experiment.

    Args:
        data (numpy.ndarray): Data to display.
    """
    im = image_exp_data(data)
    plt.imshow(im)
    plt.show()

def image_exp_data(total_data):
    """
    make data into image
    Args:
        data (numpy.ndarray): Data
    Return:
        numpy.ndarray: Image data
    """
    length_pattern = int(np.sqrt(total_data.shape[0]//2))
    measure = total_data[0::2] - total_data[1::2]
    _pixel = length_pattern**2
    hadamard_array = np.array(hadamard(_pixel))
    key = np.linalg.inv(hadamard_array.reshape(_pixel, _pixel))
    imarr = np.matmul(key, measure)
    
    return np.transpose(imarr.reshape((length_pattern, length_pattern)))




# Example usage
if __name__ == '__main__':
    # DIRECTORY = 'C:\\Users\\CHAEGYEONGJUN\\iCloudDrive\\Desktop\\test\\new0204n\\'
    # FILENAME = 'test'
    # PIXEL = [256]
    # PICTURETIME = [10000]
    # os.makedirs(DIRECTORY, exist_ok=True)

    # explist = [[DIRECTORY + f"{FILENAME}_{pixel}_{rptime}", pixel, rptime] for rptime in PICTURETIME for pixel in PIXEL]
    # for (FILENAME, pixel, picturetime) in explist:
    #     experiment(pixel, picturetime, FILENAME, _length_seq=768, _size_im=300)
    display_exp_data_file('240324_12_1024_10000_0.npy')
