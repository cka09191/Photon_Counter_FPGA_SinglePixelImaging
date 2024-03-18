import datetime as time
from tkinter import Entry, Text, Tk, Listbox
from tkinter.ttk import Frame, Label, Button, LabeledScale

class ControlPanel:
    def __init__(self):
        self.root = Tk()
        self.root.title("Experiment Control Panel")
        self.root.geometry("450x700")
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
        self.entry_pixel.insert(0, "256,1024,4096")
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
        self.queuelist.pack(expand=True, fill='both')

        # Control buttons
        self.frame_control_buttons = Frame(self.frame_queue)
        self.button_run = Button(self.frame_control_buttons, text="Run", command=self.run, width=3)
        self.button_stop = Button(self.frame_control_buttons, text="Stop", command=self.stop, width=3)
        self.button_queue_delete = Button(self.frame_control_buttons, text="Delete", command=self.delete, width=3)
        self.button_run.pack(side='left', ipadx=10)
        self.button_stop.pack(side='left', ipadx=10)
        self.button_queue_delete.pack(side='right', ipadx=10, anchor='e')
        self.frame_control_buttons.pack(side='bottom', ipadx=10, anchor='se', fill='both', expand=False)


        self.frame_queue.pack(padx=10, pady=10, fill='both', expand=True) 

        # Done list
        self.frame_done = Frame(self.frame_lists) 
        self.done_label = Label(self.frame_done, text="Done", font=("Arial", 16))
        self.done_label.pack(side='top', pady=10)
        self.done_list = Listbox(self.frame_done, height=2, width=70,selectmode="extended")
        self.done_list.pack(expand=True, fill='both')
        self.frame_done.pack(padx=10, pady=10, fill='both', expand=True)

        self.frame_lists.pack(ipady=20,padx=10, pady=10, fill='both', expand=True)

        self.root.mainloop()

        self.frame_queue = Frame(self.root)
    
    def run(self):
        pass

    def stop(self):
        pass

    def delete(self):
        delete_list = self.queuelist.curselection()
        for item in delete_list[::-1]:
            self.queuelist.delete(item)

    def add_to_queue(self):
        label = self.entry_explabel.get("1.0", "end")
        timestart, timeend, timeinterval = self.entry_time.get().split(":") 
        times = [time for time in range(int(timestart), int(timeend), int(timeinterval))]
        pixels = self.entry_pixel.get().split(",")
        repetitions = [rep for rep in range(int(self.entry_repetitions.get()))]
        totallist = [(time, pixel, repetition) for time in times for pixel in pixels for repetition in repetitions]
        
        for (time, pixel, repetition) in totallist:
            #if there is already a same item in the queue, repetition number will be added
            repetitions = self.queuelist.get(0, "end")
            while (f"{label} {time} {pixel} {repetition}") in repetitions:
                repetition += 1
            self.queuelist.insert("end", f"{label} {time} {pixel} {repetition}")



if __name__ == "__main__":
    ControlPanel()
