

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
from python_frontend.controller_dmd import controller_dmd

from python_frontend.FtdiController import FtdiController

image_data = {}

def _hadamard_image_data(_pixel: int, _reversed=False):
    """
    Generate Hadamard image as a numpy array.

    Args:
        pixel (int): Number of pixels.
        size_im (int): Size of the image.
        reversed (bool, optional): Whether to reverse the Hadamard pattern. Defaults to False.

    Returns:
        numpy.ndarray: Hadamard image array(not image)
    """
    _ = 1
    if _reversed is True:
        _ = -1

    if _pixel*_ not in image_data:
        hadamard_array = hadamard(_pixel)*_
    size = int(np.sqrt(_pixel))
    return np.reshape(np.array(hadamard_array, dtype=np.uint8), (_pixel,size,size))


def count_read_coincidance(ftdi: FtdiController, reset=False):
    histogram = count_read_histogram(ftdi, reset)
    return histogram[histogram.argmax()-1:histogram.argmax()+2].sum()
    
def count_read_histogram(ftdi: FtdiController, reset=False):
    """
    Read count data from the Ftdi controller and return as a numpy array.

    Args:
        ftdi (FtdiController): Ftdi controller object.

    Returns:
        numpy.ndarray: all count data(histogram -256ns to 254ns, bin is 2ns)
          from the Ftdi controller.

    """
    if reset:
        read_data = ftdi.write([0xFF]*1024, 1024)
    else:
        read_data = ftdi.write([0x00]*1024, 1024)

    int_data = [int.from_bytes(read_data[i:i+4], 'big') for i in range(0, 1024, 4)]
    return np.array(int_data, dtype=np.int32)

def reset_histogram(ftdi: FtdiController):
    """
    Reset the histogram in the Ftdi controller.

    Args:
        ftdi (FtdiController): Ftdi controller object.
    """
    ftdi.write([0xFF]*1024, 1024)



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

    print('fgpa initializing', end='')
    fpga_controller = FtdiController_mock()
    print('...done')

    print('Pattern and key generating', end='')
    print(f"pixel:{_pixel}, picturetime:{_picture_time}, im_size:{_size_im}")
    start_time = time.perf_counter()
    length_pattern = int(np.sqrt(_pixel))

    # hadamard_image_data_set is a set of hadamard images in two polarities
    _size= int(np.sqrt(_pixel))
    hadamard_image_data_set = np.zeros((_pixel*2, _size, _size),np.uint8)
    hadamard_image_data_set[0::2,:,:] = _hadamard_image_data(_pixel, )
    hadamard_image_data_set[1::2,:,:] = _hadamard_image_data(_pixel, True)
    
    # key is inverse of hadamard_array which is used to decode the image
    hadamard_array = np.array(hadamard(_pixel))
    key = np.linalg.inv(hadamard_array.reshape(_pixel, _pixel))
    print('...done')
    processing_time = time.perf_counter() - start_time
    print(f"processing time:{processing_time}")
    times['processing'] = processing_time

    
    print('experiment and aquisition start', end='')
    total_data = np.array([])

    # start_time is used to measure the time for the whole aquisition and communication
    start_time = time.perf_counter()
    # measure_time_total is the time for each measurement of the sequence
    list_measure_time = []
    list_communication_time = []
    # repeat until the length of the acquired data is the same as the length of the sequence
    for i in range(_pixel*2):
        measure_start_time = time.perf_counter()
        dmd.set_image(hadamard_image_data_set[i], size_im=_size_im, pattern_size=length_pattern)
        reset_histogram(fpga_controller)
        time.sleep(_picture_time/1_000_000)
        coincidance_count = count_read_coincidance(fpga_controller)
        list_measure_time.append(time.perf_counter() - measure_start_time)
        comm_start_time = time.perf_counter()
        total_data = np.append(total_data, coincidance_count)
        list_communication_time.append(time.perf_counter() - comm_start_time)
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

    print('experiment and aquisition end, disconnect FPGA and DMD', end='')
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


class FtdiController_mock(FtdiController):
    def __init__(self):
        pass

    def write(self, data, length):
        return [0]*length

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
