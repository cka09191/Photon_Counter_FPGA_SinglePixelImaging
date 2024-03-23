import threading
from control_panel import ControlPanel
from dmd_panel import DMD_Panel

def target_ctrl():
    ControlPanel("450x700+0+0")

def target_dmd():
    DMD_Panel("450x700+450+0")

if __name__ == "__main__":
    #use two threads to run the control panel and the dmd panel
    threads = []
    threads.append(threading.Thread(target=target_ctrl))
    threads.append(threading.Thread(target=target_dmd)) 
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    # ControlPanel()
    # DMD_Panel()
    # DMD = dmd_controller()