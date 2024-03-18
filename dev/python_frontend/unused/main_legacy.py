import os

import numpy as np
import time
from ALP4 import *
import imutils

import time
from scipy.linalg import hadamard
import cv2
import PowermeterManager
from ArduinoSerialCheckProtocol import ArduinoSerialCheckProtocol
from PowerMeterWithArduinoSerial import PowerMeterWithArduinoSerial
from image_process import measured_pattern_to_image

os.add_dll_directory("C:/Users/CHAEGYEONGJUN/PycharmProjects/SinglePixelImagingWithDMD")
bitDepth = 1


def setimage(DMD, img_):
    img = np.concatenate([img_, img_])
    # Allocate the onboard memory for the image sequence
    DMD.SeqAlloc(nbImg=2, bitDepth=bitDepth)
    # Send the image sequence as a 1D list/array/numpy array
    DMD.SeqPut(imgData=img)
    # Set image rate to 50 Hz
    DMD.SetTiming(pictureTime=100)

    # Run the sequence in an infinite loop
    DMD.Run()


def pattern_to_image(_pattern, _pattern_size, light=255, background=0,
                     display_size=(1920, 1080)):
    """
    :param display_size: 화면 크기
    :param backgroundrgb: 배경 rgb값
    :param rgb: 색상 rgb 값
    :param _pattern: pattern 을 rgb 255로 변경, np.uint8로 변경, 1 혹은 -1인 1차 배열
    :param _pattern_size: 패턴 크기
    :return: 이미지 np 배열, 0~255
    """
    _pattern = _pattern.reshape((_pattern_size, _pattern_size))
    _pattern = cv2.resize(np.uint8(_pattern), (min(display_size),min(display_size)))
    rotated = imutils.rotate_bound(_pattern*255, 135)
    size_im = 700
    hadamard_pattern1 = cv2.resize(rotated,(size_im,size_im), interpolation=cv2.INTER_NEAREST)
    sized = cv2.copyMakeBorder(
    hadamard_pattern1,
    top=(display_size[1]-size_im)//2,
    bottom=(display_size[1]-size_im)//2,
    left=(display_size[0]-size_im)//2,
    right=(display_size[0]-size_im)//2,
    borderType=cv2.BORDER_CONSTANT,
    value=[0, 0, 0])
    return (sized<127)*255


def pattern_to_image_continuous(_pattern, _pattern_size, rgb=(255, 255, 255),
                                display_size=(1920, 1080)):
    """
    :param display_size: 화면 크기
    :param backgroundrgb: 배경 rgb값
    :param rgb: 색상 rgb 값
    :param _pattern: pattern 을 rgb 255로 변경, np.uint8로 변경, 0~255인 배열
    :param _pattern_size: 패턴 크기
    :return: 이미지 np 배열. -~255
    """
    hadamard_pattern1 = cv2.resize(_pattern.reshape((_pattern_size, _pattern_size)),
                                   display_size,
                                   interpolation=cv2.INTER_NEAREST)
    return np.stack([rgb[0] * hadamard_pattern1,
                     rgb[1] * hadamard_pattern1,
                     rgb[2] * hadamard_pattern1],
                    axis=-1).astype(np.uint8)


# 수치##################################################################################
# 하다마드 행렬 2^2n승 해상도 수

hadamard_array_size = 1024
intensity_array = np.array(hadamard_array_size * 2)
# 측정 설정
time_between_display_and_measurement = 0
time_between_display_and_measurement_0 = 0
time_measure = 0
rep_measure = 400
wavelength_measure = 780.0

arduinoprotocol = ArduinoSerialCheckProtocol("COM7", 115200, 'E', 5, 2, 1)
powermeter = PowerMeterWithArduinoSerial(arduinoprotocol)

# slm 설정
display_size = [1024, 768]
#######################################################################################

pattern_size = int(np.sqrt(hadamard_array_size))
hadamard_array = (np.array(hadamard(hadamard_array_size)))#.astype(np.int_)
image_array = np.zeros(hadamard_array_size)

# Load the Vialux .dll
DMD = ALP4(version='4.3')
# Initialize the device
DMD.Initialize()

slm_rep = 0
xx=np.array([1,1,1,1])
zerof = pattern_to_image(xx, _pattern_size=2,
                                display_size=display_size)>127
import matplotlib.pyplot as plt
setimage(DMD, zerof*255)
plt.imshow(zerof*255, cmap='gray', vmin=0, vmax=255)
plt.show()
time_start = time.time()
hadamard_array_4 = np.vstack([hadamard_array,hadamard_array,hadamard_array,hadamard_array])
length = pattern_size
t=16
for i in range(t):
    DMD.Halt()
    DMD.FreeSeq()
    DMD.Free()
    DMD = ALP4(version='4.3')
    DMD.Initialize()
    for hadamard_basis in hadamard_array[(length**2//t)*i:(length**2//t)*(i+1)]:
        # slm에
        mean_each_measure = 0
        mean_measure = 0
        hadamard_basis.reshape([length,length])
        for is_reversed in [1, -1]:
            setimage(DMD, zerof)
            time.sleep(time_between_display_and_measurement_0)
            img = pattern_to_image(_pattern=is_reversed == hadamard_basis, _pattern_size=pattern_size,
                                   display_size=display_size)
            setimage(DMD, img)

            time.sleep(time_between_display_and_measurement)
            mean_each_measure = powermeter.mean(second=time_measure, reps=rep_measure,
                                                wavelength=wavelength_measure)
            # print()
            # setimage(DMD, zerof)
        #    time.sleep(time_between_display_and_measurement)
       #     mean_each_measure_nor = powermeter.mean(second=time_measure, reps=rep_measure,
        #    wavelength=wavelength_measure
            mean_measure += (mean_each_measure) * is_reversed
            # intensity_array = mean_each_measure
            slm_rep += 1

        image_array += hadamard_basis * mean_measure
        temp_array = image_array - image_array.min()
        max_temp_array = temp_array.max()
        temp_array /= max_temp_array if max_temp_array != 0 else 1

        ###이미지 컴퓨터 모니터 화면에 띄움##############################################
        cv2.imshow('title', np.hstack([
            pattern_to_image_continuous(
                hadamard_basis,
                pattern_size,
                display_size=(256, 256)),
            measured_pattern_to_image(
                temp_array,
                pattern_size,
                display_size=(256, 256))]))
        time_elapsed = time.time()-time_start
        cv2.setWindowTitle('title', "{}/{}, elapsed {:.1f}s, left:{:.1f}s".format(slm_rep, hadamard_array_size * 2, time_elapsed,time_elapsed/slm_rep*(hadamard_array_size * 2-slm_rep)))
        cv2.waitKey(1)
image_exp = image_array
image_array = (image_array - hadamard_array.mean() * image_array.mean())
np.save(
    'C:\\Users\\CHAEGYEONGJUN\\OneDrive - pusan.ac.kr\\바탕 화면\\research\\2023~\\pixel{} slmdelay{} measuredelay{}.npy'.format(
        hadamard_array_size, time_between_display_and_measurement, time_measure), image_array)
pixel_image_array = image_array
cal_two = pixel_image_array - pixel_image_array.min()
cal_two = cal_two / cal_two.max()
# 빈 상 출력
cv2.imshow('title', np.concatenate([pattern_to_image_continuous(np.uint8(temp_array*255),
                                                                pattern_size,
                                                                display_size=(512, 512)),
                                    pattern_to_image_continuous(np.uint8(cal_two*255),
                                                                pattern_size,
                                                                display_size=(512, 512))], axis=1))

cv2.waitKey()

# Stop the sequence display
DMD.Halt()
# Free the sequence from the onboard memory
DMD.FreeSeq()
# De-allocate the device
DMD.Free()
# #############################################
# hadamard pattern 출력 및 powermeter 로 평균 측정 후 보정이미지에 저장######################


# # hadamard pattern과 보정 이미지를 통해 실제 이미지 구하기###################################
#
# image_array = np.zeros(hadamard_array_size)
# hadamard_mean = 0
# slm_rep = 1
# for hadamard_basis in hadamard_array:
#     # slm에
#     for is_reversed in [1, -1]:
#         hadamard_mean += np.mean(hadamard_basis == is_reversed)
#
#         slm.np_data_print(
#             image_data=SLMManager.pattern_to_image(is_reversed * hadamard_basis,
#                                                    pattern_size,
#                                                    display_rgb,
#                                                    background_rgb,
#                                                    display_size=display_size),
#             x_deg=x_deg,
#             y_deg=y_deg,
#             gamma=gamma,
#             phase_wrap=phase_wrap)
#
#         time.sleep(time_between_display_and_measurement)
#         mean = powermeter.mean(second=time_measure, reps=rep_measure,
#                                wavelength=wavelength_measure)
#         image_array += (is_reversed == hadamard_basis) * mean
#         temp_array = image_array - hadamard_mean / slm_rep * image_array.mean()
#         max_temp_array = temp_array.max()
#         temp_array /= max_temp_array if max_temp_array != 0 else 1
#         temp_array_calibrated = np.clip(1+temp_array-calibration_array, 0, 1)
#         cv2.imshow('title', np.concatenate([
#             SLMManager.pattern_to_image_continuous(
#                 hadamard_basis * is_reversed,
#                 pattern_size,
#                 display_rgb,
#                 display_size=(256, 256)),
#             SLMManager.pattern_to_image(
#                 np.ones(temp_array.shape),
#                 pattern_size,
#                 (255, 0, 0),
#                 display_size=(40, 256)),
#             SLMManager.pattern_to_image_continuous(
#                 temp_array,
#                 pattern_size,
#                 display_rgb,
#                 display_size=(256, 256)),
#             SLMManager.pattern_to_image(
#                 np.ones(temp_array.shape),
#                 pattern_size,
#                 (255, 0, 0),
#                 display_size=(40, 256)),
#             SLMManager.pattern_to_image_continuous(
#                 temp_array_calibrated,
#                 pattern_size,
#                 display_rgb,
#                 display_size=(256, 256)),
#             ],
#             axis=1), )
#         cv2.setWindowTitle('title', "{}/{}".format(slm_rep+hadamard_array_size*2, hadamard_array_size*4))
#         cv2.waitKey(1)
#         slm_rep += 1
#
# image_array = (image_array - hadamard_mean / slm_rep * image_array.mean())
# image_array = np.clip(
#     a=image_array / (image_array.max()),
#     a_min=0.00000001,
#     a_max=1)
#
# image_array_calibrated = 1+image_array - calibration_array
# image_array_calibrated = np.clip(image_array_calibrated, 0, 1)
# cv2.imshow('title', np.concatenate([
#     SLMManager.pattern_to_image_continuous(
#         image_array,
#         pattern_size,
#         display_rgb,
#         display_size=(256, 256)),
#     SLMManager.pattern_to_image(
#         np.ones(temp_array.shape),
#         pattern_size,
#         (255, 0, 0),
#         display_size=(40, 256)),
#     SLMManager.pattern_to_image_continuous(
#         image_array_calibrated,
#         pattern_size,
#         display_rgb,
#         display_size=(256, 256))],
#     axis=1), )
#
# cv2.waitKey(0)
#
# """
#
# for hadamard_basis in hadamard_array:
#     slm.np_data_print(SLMManager.pattern_to_image(_pattern=hadamard_basis,
#                                                   _pattern_size=pattern_size,
#                                                   rgb=display_rgb,
#                                                   backgroundrgb=background_rgb,
#                                                   display_size=display_size),
#                       x_deg=x_deg,
#                       gamma=gamma,
#                       phase_wrap=phase_wrap)
#
#     time.sleep(time_between_display_and_measurement)
#
#     mean = powermeter.mean(second=time_measure, reps=rep_measure,
#                            wavelength=wavelength_measure)
#
#     image_array += hadamard_basis * mean
#     image_mean += mean
# image_mean /= hadamard_array_size
# image_array_calibrated = image_array / calibration_array
#
# # 가로로 이어붙여 원본과 보정이미지 출력
# cv2.imshow('image',
#            np.clip(
#                np.hstack(((image_array - image_mean * hadamard_array.mean()),
#                           (image_array_calibrated - image_mean * hadamard_array.mean()))) / (image_array.max()) * 255,
#                a_min=0,
#                a_max=255).astype(np.uint8))
# cv2.waitKey(0)
# """
