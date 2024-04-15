"""


@author Gyeongjun Chae(https://github.com/cka09191)
"""
import os
import time
import cv2
import numpy as np
from scipy.linalg import hadamard
from python_frontend.image_process import rotation, pattern_to_image

from ALP4 import ALP4, tAlpDynSynchOutGate, ALP_DEV_DYN_SYNCH_OUT1_GATE


#dll directory
os.add_dll_directory("C:/Users/CHAEGYEONGJUN/PycharmProjects/SinglePixelImagingWithDMD")


class controller_dmd:
    """
    dmd controller
    """
    def __init__(self):
        # Load the Vialux .dll
        self.dmd = ALP4(version='4.3')
        self.dmd.Initialize()
        self.bit_depth = 1
        self.set_sync()


    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.dmd.Halt()
        self.dmd.Free()



    def set_sync(self):
        """
        set the sync signal
        """
        gate = tAlpDynSynchOutGate()
        gate.Period = 1
        gate.Polarity = 0
        gate.Gate[0] = 1
        self.dmd.DevControlEx(ALP_DEV_DYN_SYNCH_OUT1_GATE, gate)

    def set_image(self, array, _bit_depth = 1, pic=1000,pattern_size=2,size_im=543,repeat=True):
        """
        display the image
        """
        img_data = self.array_set_to_imagedata([array,array],pattern_size,size_im=size_im)
        self.this_slide_show(img_data, 16, _bit_depth, pic, repeat)

    def simple_test(self, array = None,pic = 1000,pattern_size=2,size_im=543,repeat=True):
        """
        test
        """
        if array is None:
            array = [1,0,1,0]
        self.set_image(array, pic=pic, pattern_size=pattern_size,size_im=size_im,repeat=repeat)

    def this_slide_show(self, imgData, nbImg, bitDepth, pictureTime, loop):
        if nbImg>100:
            raise Exception("nbImg Over 100")
        buff = (np.array(imgData==0)*255)

        # Allocate the onboard memory for the image sequence
        self.dmd.SeqAlloc(nbImg=len(buff), bitDepth=bitDepth)
        # Send the image sequence as a 1D list/array/numpy array
        self.dmd.SeqPut(imgData=buff)

        self.dmd.SetTiming(pictureTime=pictureTime)
        # Run the sequence in an infinite loop

        # self.DMD.ProjControl(ALP_PROJ_STEP, ALP_EDGE_FALLING)
        self.dmd.Run(loop=loop)

        # self.DMD.FreeSeq()

    def Freeseq(self, SequenceIds):
        for sequenceId in SequenceIds:
            self.dmd.FreeSeq(SequenceId=sequenceId)

    def slideshow(self, pictureTime, SequenceId, loop):
        self.dmd.SetTiming(SequenceId=SequenceId, pictureTime=pictureTime)
        # Run the sequence in an infinite loop
        self.dmd.Run(loop=loop, SequenceId=SequenceId)
    def upload(self, imgData, nbImg, bitDepth,seq_length=100):
        last = len(self.dmd.Seqs)
        for nb in range(0, nbImg, seq_length):
            imgsmallbuff = (imgData[nb:nb + seq_length,:,:]<128)*255
            # Allocate the onboard memory for the image sequence
            # print(f"state{imgsmallbuff.shape}")
            self.dmd.SeqAlloc(nbImg=len(imgsmallbuff), bitDepth=bitDepth)
            # Send the image sequence as a 1D list/array/numpy array
            self.dmd.SeqPut(imgData=imgsmallbuff)
        return (self.dmd.Seqs[last:])


    @classmethod
    def image_sizer(cls, img_,display_size=(1024,768)):
        sized = cv2.copyMakeBorder(
            img_,
            top=(display_size[1] - img_.shape[1]) // 2 + (display_size[1] - img_.shape[1]) % 2,
            bottom=(display_size[1] - img_.shape[1]) // 2,
            left=(display_size[0] - img_.shape[0]) // 2 + (display_size[0] - img_.shape[0]) % 2,
            right=(display_size[0] - img_.shape[0]) // 2,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0])
        return sized

    @classmethod
    def array_set_to_imagedata_each_process(cls, array_set, _pattern_size, size_im, index, result_dict):
        result_dict[index] = cls.array_set_to_imagedata(array_set,_pattern_size,size_im)

    @classmethod
    def array_set_to_imagedata(cls, array_set,
                                _pattern_size,size_im=543,rot = 0):
        # if array_set.shape[-1]>1000:
        #     manager = multiprocessing.Manager()
        #     result_dict = manager.dict()
        #     procs = []
        #     indexlist = [index for index in range(0,array_set.shape[-1],1000)]
        #     for index in indexlist:
        #         indexlist.append(index)
        #         array_set_buff = array_set[index:index+1000].copy()
        #         p = multiprocessing.Process(target=cls.array_set_to_imagedata_each_process, args=[array_set_buff, _pattern_size, size_im, index, result_dict])
        #         p.start()
        #
        #     for j in procs:
        #         j.join()
        #     result = []
        #     for index in indexlist:
        #         result+=result_dict[index]
        #     return result

        imgData = [cls.image_sizer(rotation(pattern_to_image(np.array(array_each), _pattern_size, size_im=size_im),angle=rot)[:, :, 0])
             for array_each in array_set]
        return np.array(imgData)
    def wait(self):
        self.dmd.Wait()

def new_array_image_data(pixel:int):
    directory = 'C:\\Users\\CHAEGYEONGJUN\\iCloudDrive\\Desktop\\Test\\new_array\\'
    os.makedirs(directory, exist_ok=True)
    filename = f'{pixel}.npy'
    if filename in os.listdir(directory):
        return np.load(directory+filename)
    else:
        new_array =hadamard(pixel) ==1
        new_array[0::2,0] = False
        hadamard_array = np.array(new_array,dtype=np.int32)
        pixel_sqrt_is_length = int(np.sqrt(pixel))
        imgData = dmd_controller.array_set_to_imagedata(hadamard_array, pixel_sqrt_is_length, size_im=200)
        np.save(directory+filename,imgData)
        return np.array(imgData)

if __name__ == "__main__":
    DMD = dmd_controller()
    # DMD.simpletest(array=[int(9000>x>8000) for x in range(16384)], pattern_size=128, pic=10000000)
    from ALP4 import ALP_DDC_FPGA_TEMPERATURE
    # DMD.simpletest(array=[int(y%256<128)for x in range(1024) for y in range(1024)], pattern_size=1024, pic=10000000)
    print('temp')
    print(    DMD.dmd.DevInquire(ALP_DDC_FPGA_TEMPERATURE)/256)
    # DMD.DMD.ProjControl(ALP_PROJ_INVERSION, ALP_PROJ_INVERSIONnot ALP_DEFAULT)
    DMD.simple_test(array=[1,0,1,1], pattern_size=2, pic=1000, size_im=50)
    pixel = 2
    # new_array = DMD.array_set_to_imagedata([[[0]*50+[1]+[0]*50]*50+[[1]*101]+[[0]*50+[1]+[0]*50]*50],101,543)
    # new_array = DMD.array_set_to_imagedata([[[0]*pp+[1]+[0]*pp]*pp+[[1]*(2*pp+1)]+[[0]*pp+[1]+[0]*pp]*pp,[[0]*pp+[1]+[0]*pp]*pp+[[1]*(2*pp+1)]+[[0]*pp+[1]+[0]*pp]*pp],(2*pp+1),300,rot=135)
    # new_array = np.concatenate((new_array, DMD.array_set_to_imagedata([[[0,1,0,0]*4+[0,0,0,0]*4]*8],16,50)))
    # new_array = np.concatenate((new_array, DMD.array_set_to_imagedata([[[1,1,1,1]*4+[1,1,1,1]*4]*8],16,50)))
    # new_array = DMD.array_set_to_imagedata([[0]*x+[1]+[0]*(pixel*pixel-x-1) for x in range(pixel*pixel)],pixel,500)
    # new_array[new_array == 0] = -1
    Gate = tAlpDynSynchOutGate()
    Gate.Period = 1
    Gate.Polarity = 1
    Gate.Gate[0] = 1
    DMD.dmd.DevControlEx(ALP_DEV_DYN_SYNCH_OUT1_GATE, Gate)
    print('res')
    # DMD.this_slide_show(new_array, pixel, 4, 8000000, True)
    # DMD.simpletest()
    # print(new_array.shape)
    # DMD.simpletest(array=[[1,0,1,0],[0,0,0,0]],pic=100000)
    # DMD.wait()
    # array_set = []
    # sd=2**4
    # sd2 = sd**2
    # for i in range(sd2):
    #     t = [0 for x in range(sd2)]
    #     t[i % sd2] = 1
    #     array_set.append(t)
    # imgData = DMD.array_set_to_imagedata(np.array(array_set),sd)
    # print(imgData.shape)
    # print(len(imgData))
    # for j in range(100):
    #     tt = time.perf_counter()
    #     slides = DMD.upload(imgData, len(imgData), 1)
    #     print(slides)
    #     for slide in slides:
    #         DMD.this_slide_show(DMD.array_set_to_imagedata([[0,0,0,0],[1,1,1,1]], 2),2,1,100000,False)
    #         print("aa")
    #         DMD.wait()
    #     DMD.Freeseq(slides)
    #     print(time.perf_counter()-tt)


    time.sleep(50000)
    # print(time.perf_counter()-tt)

