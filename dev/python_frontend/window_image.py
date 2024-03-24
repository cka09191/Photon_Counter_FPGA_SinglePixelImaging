
import os
from tkinter import Checkbutton, IntVar, Label, Tk, PhotoImage, Listbox, Entry, Button, filedialog, Frame
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pickle

import experiment

class window_image:
    def __init__(self ,geometry="250x750+10+10", image=None):
        self.width, self.height = map(int, geometry.split("+").pop(0).split("x"))

        self.root = Tk()
        self.root.title("Image Aquired")
        self.root.geometry(geometry)
        self.listbox_file = Listbox(self.root, selectmode="single")
        #when mouse release
        self.listbox_file.bind("<ButtonRelease-1>", self.click_filename)
        self.image_original = image
        self.frame_folder = Frame(self.root)
        self.entry_foldername = Entry(self.frame_folder)
        self.button_foldername = Button(self.frame_folder, text="Folder Name", command=self.get_foldername)
        self.button_refresh = Button(self.frame_folder, text="Refresh", command=self.refresh)
        self.gray = IntVar()
        self.checkbox_gray = Checkbutton(self.frame_folder, text="Gray", variable=self.gray)
        self.button_foldername.pack(side="left", anchor="center")
        self.entry_foldername.pack(side="left", anchor="center")
        self.button_refresh.pack(side="left", anchor="center")
        self.checkbox_gray.pack(side="left", anchor="center")

        self.frame_folder.pack(side="top", anchor="center")

        self.listbox_file.pack(fill="both", expand=True, side="top", anchor="center", )
        
        self.label_information = Label(self.root, text="Click on the file to display the image")
        self.label_information.pack(side="top", anchor="w")

        self.frame_canvas = Frame(self.root)
        self.figure = plt.Figure(figsize=(self.width//100, self.height//100), dpi=100)
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_canvas)
        self.canvas.get_tk_widget().pack(side="bottom", anchor="center", fill="both", expand=True)
        self.frame_canvas.pack(side="bottom", anchor="center", fill="both", expand=True)

        self.show_image()


        self.root.mainloop()
    
    def click_filename(self, event):
        filename = self.listbox_file.get(self.listbox_file.curselection())
                                         
        foldername = self.entry_foldername.get()
        self.image_original = np.load(os.path.join(foldername, filename))
        self.show_image()

        pickle_time_location =os.path.join(foldername,filename[:-4]+"_exp")
        with open(pickle_time_location, 'rb') as f:
            times = pickle.load(f)
        
        total_measure = sum(times['measure_time'])
        total_communication = sum(times['communication_time'])
        self.label_information.config(text=f"measure time\t\t:{total_measure:10.3f}s\ncommunication time\t:{total_communication:10.3f}s")


    def get_foldername(self):
        filename = filedialog.askdirectory()
        self.entry_foldername.delete(0, "end")
        self.entry_foldername.insert(0, filename)
        self.refresh()
    
    def refresh(self):
        foldername = self.entry_foldername.get()
        self.listbox_file.delete(0, "end")
        for file in os.listdir(foldername):
            if file.endswith(".npy"):
                self.listbox_file.insert("end", file)


    def show_image(self):
        if self.image_original is not None:
            imadge_calculated = experiment.image_exp_data(self.image_original)
            zoomrate = self.width//int(np.sqrt((self.image_original.shape[0]//2)))
            self.figure.clear()
            ax = self.figure.add_subplot(3,1,(1,2))
            color = None
            if self.gray.get() == 1:
                color = "gray"

            ax.imshow(imadge_calculated, cmap=color)
            length = int(np.sqrt(self.image_original.shape[0]//2))
            image_raw = self.image_original.reshape((length, 2*length))
            ax = self.figure.add_subplot(3,1,3)
            ax.imshow(image_raw, cmap=color)
            self.canvas.draw()



        else:
            print("No image to show")





if __name__ == "__main__":
    window = window_image(geometry="250x750+10+10")