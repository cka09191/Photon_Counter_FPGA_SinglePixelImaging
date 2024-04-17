import time
from tkinter import Entry, Tk, filedialog
from tkinter.ttk import Label, Button
from threading import Thread, Event
from pyftdi.spi import SpiController

class window_control:
    def __init__(self, _window):
        self.window = _window
        self.window.title("simple counter")
        self.window.geometry("400x300")
        self.label = Label(self.window, text="simple counter")
        self.label.pack()
        self.button = Button(self.window, text="Open File", command=self.open_file)
        self.button.pack()
        self.label = Label(self.window, text="File Path:")
        self.entry = Entry(self.window)
        self.entry.insert(0,"C:/Photon_Counter_FPGA/Photon_Counter_FPGA/dev/fpga/rough_Time_Corelation_Analizer/frontend_python/my.txt.txt")
        self.entry.pack()
        self.label2 = Label(self.window, text="Count bin(ms):")
        self.entry2 = Entry(self.window)
        self.entry2.insert(0,"1000")
        self.button2 = Button(self.window, text="start_count", command=self.start_count)
        self.label2.pack()
        self.entry2.pack()
        self.button2.pack()
        self.thread_event_stop = Event()
        self.thread = None
        self.thread_event_stop.set()
        self.button3 = Button(self.window, text="stop_count", command=self.thread_event_stop.set)
        self.button3.pack()


    def open_file(self):
        file_path = filedialog.asksaveasfilename()
        self.entry.insert(0, file_path)
    
    def start_count(self):

        time_bin = int(self.entry2.get().strip())
        file_path = self.entry.get()
        self.thread_event_stop.clear()
        self.thread = Thread(target=thread_count, args=(time_bin, file_path, self.thread_event_stop))
        print(file_path)
        print("start count")
        self.thread.start()


def thread_count(time_bin, file_path, thread_event_stop):
    controller = ftdi_controller()
    while(not thread_event_stop.is_set()):
        count = controller.write([0x00]*511+[0x00],512)
        str_bins = ""
        bins = []
        for i in range(0, count.__len__(), 4):
            bin_int = int.from_bytes(count[i:i+4], "big", signed=False)
            bins.append(bin_int)
            str_bins += str(bin_int) + ", "
        str_bins= str_bins.removesuffix(", ")
        print("thisiscount")
        print(str_bins)
        file = open(file_path, "w", encoding="utf-8")
        file.write(str_bins)
        #show plot in 1 sec
        plt.plot(range(0, bins.__len__()), bins)
        # count = controller.write([0x00]*511+[0xFF],512)
        plt.show(block=False)
        plt.pause(time_bin/1000)
        plt.close()
        file.close()



    print("end count")

class ftdi_controller:
    def __init__(self):
        self.spi = SpiController(cs_count=2)
        self.spi.configure('ftdi://ftdi:232h/1')
        self.port = self.spi.get_port(1, freq=1e6, mode=0)
    
    def write(self, data, length):
        data = self.port.exchange(data, length)
        return data


if __name__ == "__main__":
    window = Tk()
    window_control(window)
    window.mainloop()
