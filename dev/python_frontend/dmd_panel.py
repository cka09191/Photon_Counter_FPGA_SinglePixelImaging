import tkinter as tk
import numpy as np

from dmd_controller import dmd_controller

class Sketchpad(tk.Canvas):
    def __init__(self, parent, resolution=50, size=200, width=300, height=300, **kwargs):
        super().__init__(parent, width=width, height = height,**kwargs)
        self.width = width
        self.height = height
        self.resolution = resolution
        self.bind("<Button-1>", self.save_posn)
        self.bind("<B1-Motion>", self.add_line)
        self.size = size

        
    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y

    def set_resolution(self, resolution):
        self.resolution = resolution
    def get_rect_size(self):
        rect_size = self.size/self.resolution*self.width/self.size
        return rect_size
    def add_line(self, event):
        rect_size = self.get_rect_size()
        lastx_n = self.lastx//rect_size*rect_size
        lasty_n = self.lasty//rect_size*rect_size
        x_n = event.x//rect_size*rect_size
        y_n = event.y//rect_size*rect_size
        self.create_rectangle(lastx_n, lasty_n, x_n+rect_size, y_n+rect_size, fill="red", outline="red", tags="rectangle",)
        self.create_line(self.lastx, self.lasty, event.x, event.y, fill="black", tags="original")
        self.save_posn(event)
    
    def clear(self):
        self.delete("all")

    def redraw(self):
        self.delete("rectangle")
        image = self.find_withtag("original")
        rect_size = self.get_rect_size()
        for item in image:
            coords = self.coords(item)
            lastx_n = coords[0]//rect_size*rect_size
            lasty_n = coords[1]//rect_size*rect_size
            x_n = coords[2]//rect_size*rect_size
            y_n = coords[3]//rect_size*rect_size
            self.create_rectangle(lastx_n, lasty_n, x_n+rect_size, y_n+rect_size, fill="red",outline="red", tags="rectangle")

    def get_array(self):
        rect_size = self.get_rect_size()
        array = np.zeros((self.resolution, self.resolution))
        for item in self.find_withtag("rectangle"):
            coords = self.coords(item)
            x = int(coords[0]//rect_size)
            y = int(coords[1]//rect_size)
            if x < self.resolution and y < self.resolution:
                array[y, x] = 1
        return array

class DMD_Panel:
    def __init__(self,geometry="400x550+800+100"):
        self.root = tk.Tk()
        self.root.title("DMD Panel")
        
        #location of the window is set to the center of the screen
        self.root.geometry(geometry)

        self.DMD=None
        self.scale_imsize = tk.Scale(self.root, from_=10, to=543, orient=tk.HORIZONTAL, resolution=10, label="Size of Image", length=200, tickinterval=200, sliderlength=20, variable=tk.IntVar(value=300), command=self.set_resolution)

        self.scale_resolution = tk.Scale(self.root, from_=4, to=512, orient=tk.HORIZONTAL, resolution=1, label="Resolution", length=200, tickinterval=100, sliderlength=20, variable=tk.IntVar(value=50), command=self.set_resolution)

        self.label = tk.Label(self.root, text="DMD Panel")
        self.frame_sketchpad = tk.Frame(self.root, background="white", border=1, relief=tk.SUNKEN)
        self.sketchpad = Sketchpad(self.frame_sketchpad, width=300, height=300)
        
        self.fram_buttom = tk.Frame(self.root)
        self.button_clear = tk.Button(self.fram_buttom, text="Clear", command=self.sketchpad.clear)
        self.button_display = tk.Button(self.fram_buttom, text="Display", command=self.display)
        self.button_stop = tk.Button(self.fram_buttom, text="Stop", command=self.stop)


        self.label.pack(side=tk.TOP)
        self.scale_imsize.pack(side=tk.TOP)
        self.scale_resolution.pack(side=tk.TOP)
        self.frame_sketchpad.pack(side=tk.TOP, padx=10, pady=10)
        self.sketchpad.pack(side=tk.TOP,)
        self.fram_buttom.pack(side=tk.BOTTOM)
        self.button_clear.pack(side=tk.LEFT)
        self.button_display.pack(side=tk.LEFT)
        self.button_stop.pack(side=tk.LEFT)
        self.root.mainloop()
    def set_resolution(self, event=None):
        self.sketchpad.set_resolution(self.scale_resolution.get())
        self.sketchpad.redraw()

    def clear_sketchpad(self, event=None):
        self.sketchpad.delete("all")
        self.sketchpad.size=int(self.scale_imsize.get())
    def display(self):
        if self.DMD:
            self.DMD.__exit__()
        self.DMD = dmd_controller()
        size_im = self.scale_imsize.get()
        array = self.sketchpad.get_array()
        print(array)
        self.DMD.simple_test(array=array, pattern_size=self.scale_resolution.get(), pic=1000, size_im=size_im)
    
    def stop(self):
        if self.DMD:
            self.DMD.__exit__()

if __name__ == "__main__":
    DMD_Panel()


# if __name__ == "__main__":
#     DMD = dmd_controller()
#     # DMD.simpletest(array=[int(9000>x>8000) for x in range(16384)], pattern_size=128, pic=10000000)
#     from ALP4 import ALP_DDC_FPGA_TEMPERATURE
#     # DMD.simpletest(array=[int(y%256<128)for x in range(1024) for y in range(1024)], pattern_size=1024, pic=10000000)
#     print('temp')
#     print(    DMD.dmd.DevInquire(ALP_DDC_FPGA_TEMPERATURE)/256)
#     # DMD.DMD.ProjControl(ALP_PROJ_INVERSION, ALP_PROJ_INVERSIONnot ALP_DEFAULT)
#     DMD.simple_test(array=[1,0,1,1], pattern_size=2, pic=1000, size_im=50)
#     pixel = 2
#     # new_array = DMD.array_set_to_imagedata([[[0]*50+[1]+[0]*50]*50+[[1]*101]+[[0]*50+[1]+[0]*50]*50],101,543)
#     # new_array = DMD.array_set_to_imagedata([[[0]*pp+[1]+[0]*pp]*pp+[[1]*(2*pp+1)]+[[0]*pp+[1]+[0]*pp]*pp,[[0]*pp+[1]+[0]*pp]*pp+[[1]*(2*pp+1)]+[[0]*pp+[1]+[0]*pp]*pp],(2*pp+1),300,rot=135)
#     # new_array = np.concatenate((new_array, DMD.array_set_to_imagedata([[[0,1,0,0]*4+[0,0,0,0]*4]*8],16,50)))
#     # new_array = np.concatenate((new_array, DMD.array_set_to_imagedata([[[1,1,1,1]*4+[1,1,1,1]*4]*8],16,50)))
#     # new_array = DMD.array_set_to_imagedata([[0]*x+[1]+[0]*(pixel*pixel-x-1) for x in range(pixel*pixel)],pixel,500)
#     # new_array[new_array == 0] = -1
#     Gate = tAlpDynSynchOutGate()
#     Gate.Period = 1
#     Gate.Polarity = 1
#     Gate.Gate[0] = 1
#     DMD.dmd.DevControlEx(ALP_DEV_DYN_SYNCH_OUT1_GATE, Gate)
#     print('res')
#     # DMD.this_slide_show(new_array, pixel, 4, 8000000, True)
#     # DMD.simpletest()
#     # print(new_array.shape)
#     # DMD.simpletest(array=[[1,0,1,0],[0,0,0,0]],pic=100000)
#     # DMD.wait()
#     # array_set = []
#     # sd=2**4
#     # sd2 = sd**2
#     # for i in range(sd2):
#     #     t = [0 for x in range(sd2)]
#     #     t[i % sd2] = 1
#     #     array_set.append(t)
#     # imgData = DMD.array_set_to_imagedata(np.array(array_set),sd)
#     # print(imgData.shape)
#     # print(len(imgData))
#     # for j in range(100):
#     #     tt = time.perf_counter()
#     #     slides = DMD.upload(imgData, len(imgData), 1)
#     #     print(slides)
#     #     for slide in slides:
#     #         DMD.this_slide_show(DMD.array_set_to_imagedata([[0,0,0,0],[1,1,1,1]], 2),2,1,100000,False)
#     #         print("aa")
#     #         DMD.wait()
#     #     DMD.Freeseq(slides)
#     #     print(time.perf_counter()-tt)


#     time.sleep(50000)
#     # print(time.perf_counter()-tt)