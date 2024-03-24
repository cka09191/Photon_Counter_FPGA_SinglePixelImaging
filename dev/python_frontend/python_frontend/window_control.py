'''


@author Gyeongjun Chae(https://github.com/cka09191)
'''
import datetime as time
import os
from pathlib import Path
import threading
from tkinter import Entry, Text, Tk, Listbox, filedialog
from tkinter.ttk import Frame, Label, Button

from  python_frontend.experiment import experiment
from python_frontend.window_image import window_image


class window_control:
    def __init__(self,geometry="450x700"):
        self.threads = []
        self._stop_event = threading.Event()
        self.root = Tk()
        self.root.title("Experiment Control Panel")
        self.root.geometry(geometry)
        self.root.minsize(400, 600)
        self.frame_settings = Frame(self.root)

        self.sub_frame_settings = Frame(self.frame_settings)
        self.label_settings = Label(self.sub_frame_settings, text="Settings", font=("Arial", 16))
        self.label_settings.pack(side='top', pady=10)

        # Time setting
        self.sub_sub_frame_settings_time = Frame(self.sub_frame_settings)
        self.label_time_frame = Frame(self.sub_sub_frame_settings_time)
        self.label_time = Label(self.label_time_frame, text="time (us):")
        self.label_time.pack(side='top',fill='both', expand=True)
        self.label_time_frame.pack(side='top',fill='both', expand=True)

        self.frame_entry_time = Frame(self.sub_sub_frame_settings_time)
        self.entry_time = Entry(self.frame_entry_time, width=9)
        self.entry_time.insert(0, "1000:2000:100")
        self.entry_time.pack(side='top',fill='both', expand=True)
        self.frame_entry_time.pack(side='top',fill='both', expand=True)

        self.sub_sub_frame_settings_time.pack(side='left',fill='both', expand=True)

        
        # Pixel setting
        self.sub_sub_frame_settings_pixel = Frame(self.sub_frame_settings)
        self.label_pixel_frame = Frame(self.sub_sub_frame_settings_pixel)
        self.label_pixel = Label(self.label_pixel_frame, text="pixels:")
        self.label_pixel.pack(side='top',fill='both', expand=True)
        self.label_pixel_frame.pack(side='top',fill='both', expand=True)

        self.frame_entry_pixel = Frame(self.sub_sub_frame_settings_pixel)
        self.entry_pixel = Entry(self.frame_entry_pixel, width=9)
        self.entry_pixel.insert(0, "64,256,1024")
        self.entry_pixel.pack(side='top',fill='both', expand=True)
        self.frame_entry_pixel.pack(side='top',fill='both', expand=True)

        self.sub_sub_frame_settings_pixel.pack(side='left',fill='both', expand=True)

        # Repetitions setting
        self.sub_sub_frame_settings_repetitions = Frame(self.sub_frame_settings)
        self.label_repetitions_frame = Frame(self.sub_sub_frame_settings_repetitions)
        self.label_repetitions_label = Label(self.label_repetitions_frame, text="repetitions:")
        self.label_repetitions_label.pack(side='top',fill='both', expand=True)
        self.label_repetitions_frame.pack(side='top',fill='both', expand=True)

        self.frame_entry_repetitions = Frame(self.sub_sub_frame_settings_repetitions)
        self.entry_repetitions = Entry(self.frame_entry_repetitions, width=9)
        self.entry_repetitions.insert(0, "1")
        self.entry_repetitions.pack(side='top',fill='both', expand=True)
        self.frame_entry_repetitions.pack(side='top',fill='both', expand=True)

        self.sub_sub_frame_settings_repetitions.pack(side='left',fill='both', expand=True)

        self.sub_frame_settings.pack(padx=10, pady=10, fill='both', expand=False)

        
        # image size setting
        self.sub_frame_imagesize = Frame(self.frame_settings)
        self.label_imagesize = Label(self.sub_frame_imagesize, text="image size:")
        self.entry_imagesize = Text(self.sub_frame_imagesize, height=1, width=10, font=("Arial", 16))
        self.entry_imagesize.insert(1.0, "300")
        self.label_imagesize.pack(side='left')
        self.entry_imagesize.pack(side='left',fill='both', expand=True)
        self.sub_frame_imagesize.pack(side='top')



        # Experiment label setting
        self.sub_frame_label = Frame(self.frame_settings)
        self.label_explabel = Label(self.sub_frame_label, text="experiment label:")
        self.label_explabel.pack(side='left')
        self.entry_explabel = Text(self.sub_frame_label, height=1, width=10, font=("Arial", 16))
        self.entry_explabel.pack(side='left',fill='both', expand=True)
        self.entry_explabel.insert(1.0, f"{time.datetime.now().strftime('%y%m%d_%H')}")
        self.sub_frame_label.pack(ipadx=40,side='left')


        # Add to queue button
        self.button_frame = Frame(self.frame_settings)
        self.addbutton = Button(self.button_frame, text="Add to Queue", command=self.add_to_queue)
        self.addbutton.pack(side='right', anchor='se')  # Set the button to the right side
        self.button_frame.pack(ipadx=50,side='right', anchor='se')

        

        
        
        self.frame_settings.pack(padx=10, pady=10, ipadx=30, expand=False)

        # Queue list
        self.frame_lists = Frame(self.root)
        self.frame_queue = Frame(self.frame_lists)
        self.queue_label = Label(self.frame_queue, text="Queue", font=("Arial", 16))
        self.queue_label.pack(side='top', pady=10)
        self.queuelist = Listbox(self.frame_queue, height=2, width=70,selectmode="extended")
        

        # Control buttons
        self.frame_control_buttons = Frame(self.frame_queue)
        self.button_run = Button(self.frame_control_buttons, text="Run", command=self.run, width=3)
        self.button_repeat = Button(self.frame_control_buttons, text="Repeat", command=self.repeat, width=3)
        self.button_queue_delete = Button(self.frame_control_buttons, text="Delete", command=self.delete, width=3)
        self.button_run.pack(side='left', ipadx=10)
        self.button_repeat.pack(side='left', ipadx=10)
        self.button_queue_delete.pack(side='right', ipadx=10, anchor='e')
        self.frame_control_buttons.pack(side='bottom', ipadx=10, anchor='se', fill='both', expand=False)


        self.frame_queue.pack(padx=10, pady=10, fill='both', expand=True)
        
        # save directory setting
        self.sub_frame_savedir = Frame(self.frame_lists)
        self.label_savedir = Label(self.sub_frame_savedir, text="save directory:")
        self.label_savedir.pack(side='left')
        self.entry_savedir = Text(self.sub_frame_savedir, height=1, width=25, font=("Arial", 16))
        self.button_savedir = Button(self.sub_frame_savedir, text="...", command=self.filedialog_savedir)
        self.entry_savedir.pack(side='left', fill='both',expand=True, ipadx=10)
        self.button_savedir.pack(side='right',fill='both', expand=True)
        self.entry_savedir.insert(1.0, f"{time.datetime.now().strftime('%y%m%d_%H')}")
        self.sub_frame_savedir.pack(expand=False)
        self.queuelist.pack(expand=True, fill='both')

        # Done list
        self.frame_done = Frame(self.frame_lists) 
        self.done_label = Label(self.frame_done, text="Done", font=("Arial", 16))
        self.done_label.pack(side='top', pady=10)
        self.done_list = Listbox(self.frame_done, height=2, width=70,selectmode="extended")
        self.done_list.pack(expand=True, fill='both')
        self.frame_done.pack(padx=10, pady=10, fill='both', expand=True)

        self.frame_lists.pack(ipady=20,padx=10, pady=10, fill='both', expand=True)

        self.root.mainloop()

    def target_repeat(self):
        """Repeat the selected items in the queue list."""
        list_repeat = self.queuelist.curselection()
        while(self._stop_event.is_set() == False and len(list_repeat) > 0):
            for item in list_repeat:
                item_each = self.queuelist.get(item)
                label, picturetime, pixel, size_im, repetition = item_each.split(" ")
                # experiment.experiment(int(pixel), int(picturetime), filename=None, _length_seq=768, _size_im=int(size_im))
                import numpy as np

            image = np.random.randint(0, 255, (450, 450))
            window = window_image()

            import time
            def target_close_window(window):
                time.sleep(5)
                window.__exit__()
            threading.Thread(target=target_close_window, args=(window,)).start()
            window.mainloop()
            

            time.sleep(5)

            # item_each = self.queuelist.get(item)
            # label, picturetime, pixel, size_im, repetition = item_each.split(" ")
            # directory = Path(self.entry_savedir.get("1.0", "end").strip('\n'))
            # filename = directory / f"{label}_{pixel}_{picturetime}_{repetition}"
            # print(f"Running {filename}")
            # experiment.experiment(int(pixel), int(picturetime), filename, _length_seq=768, _size_im=int(size_im))
            # self.queuelist.delete(item)

    def repeat(self):
        """Repeat the selected items in the queue list."""
        item = self.queuelist.curselection()[0]
        item_each = self.queuelist.get(item)
        label, picturetime, pixel, size_im, repetition = item_each.split(" ")
        experiment(int(pixel), int(picturetime), None, _length_seq=768, _size_im=int(size_im))



    def filedialog_savedir(self):
        """Open a file dialog to select a directory and insert the path to the entry widget."""
        self.entry_savedir.delete(1.0, "end")
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        self.entry_savedir.insert(1.0, filedialog.askdirectory(parent=self.root,initialdir=desktop_dir,title='Please select a directory'))
        
        # find files from the directory
        self.done_list.delete(0, "end")
        for file in os.listdir(self.entry_savedir.get("1.0", "end").strip('\n')):
            if file.endswith(".npy"):
                each = file.split("_")
                label, pixel, picturetime, size_im, repetition = "_".join(each[0:-4]), each[-4], each[-3], each[-2], each[-1].split(".")[0]
                total_label = f"{label} {pixel} {picturetime} {size_im} {repetition}"
                self.done_list.insert("end", total_label)
        
        #if there is same item in the queue, repetition number will be added
        if self.queuelist.size() > 0:
           i = 0
           while True:
                left_list = []
                left_list.extend(self.queuelist.get(i+1, "end"))
                left_list.extend(self.done_list.get(0, "end"))
                if self.queuelist.get(i) in left_list:
                    left_list = []
                    label, pixel, picturetime, size_im, repetition = self.queuelist.get(i).split(" ")
                    self.queuelist.delete(i)
                    self.queuelist.insert(i, f"{label} {pixel} {picturetime} {size_im} {int(repetition)+1}")
                else:
                    i += 1
                    if i == self.queuelist.size():
                        break
            
    def run(self):
        """Run the selected experiment with the queue list."""
        list_run = self.queuelist.curselection()
        done_list = []
        for item in list_run:
            item_each = self.queuelist.get(item)
            label, picturetime, pixel, size_im, repetition = item_each.split(" ")
            try:
                #if directory is valid
                if not os.path.exists(self.entry_savedir.get("1.0", "end").strip('\n')):
                    raise Exception("Invalid directory")
                directory = Path(self.entry_savedir.get("1.0", "end").strip('\n'))
                filename = directory / f"{label}_{picturetime}_{pixel}_{size_im}_{repetition}"
                experiment(int(pixel), int(picturetime), filename, _length_seq=768, _size_im=int(size_im))
                done_list.append(item)
            except Exception as e:
                print(e)
                print(self.entry_savedir.get("1.0", "end").strip('\n'))
        
        for item in done_list[::-1]:
            self.done_list.insert("end", self.queuelist.get(item))
            self.queuelist.delete(item)
                

        

    def delete(self):
        """Delete the selected items in the queue list."""
        delete_list = self.queuelist.curselection()
        for item in delete_list[::-1]:
            self.queuelist.delete(item)

    def add_to_queue(self):
        """Add the settings to the queue list."""
        label = self.entry_explabel.get("1.0", "end").strip('\n')
        timestart, timeend, timeinterval = self.entry_time.get().split(":") 
        times = [time for time in range(int(timestart), int(timeend), int(timeinterval))]
        pixels = self.entry_pixel.get().split(",")
        repetitions = [rep for rep in range(int(self.entry_repetitions.get()))]
        size_im = self.entry_imagesize.get("1.0", "end").strip('\n')
        totallist = [(time, pixel, repetition, size_im) for time in times for pixel in pixels for repetition in repetitions]
        for (_time, pixel, repetition, size_im) in totallist:
            #if there is already a same item in the queue, repetition number will be added
            repetitions = []
            repetitions.extend(self.queuelist.get(0, "end"))
            repetitions.extend(self.done_list.get(0, "end"))
            while (f"{label} {_time} {pixel} {size_im} {repetition}") in repetitions:
                repetition += 1
            self.queuelist.insert("end", f"{label} {_time} {pixel} {size_im} {repetition}")



if __name__ == "__main__":
    ControlPanel()
