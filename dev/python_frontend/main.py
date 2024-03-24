from multiprocessing import Process
from threading import Thread
from python_frontend.window_control import window_control
from python_frontend.window_dmd import window_dmd
from python_frontend.window_image import window_image
def target_ctrl():
    window_control("450x700+0+0")

def target_dmd():
    window_dmd("450x700+450+0")

def target_image():
    window_image("450x700+900+0")

if __name__ == "__main__":
    # target_image()
    # target_dmd()
    # target_ctrl()
    #use two threads to run the control panel and the dmd panel
    processes = []
    processes.append(Process(target=target_ctrl))
    processes.append(Thread(target=target_dmd))
    processes.append(Thread(target=target_image))
    for process in processes:
        process.start()
    for process in processes:   
        process.join()

