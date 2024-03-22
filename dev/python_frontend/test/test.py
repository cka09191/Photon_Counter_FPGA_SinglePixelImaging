import multiprocessing
import time


class item:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def print_item(self):
        print(f"{self.name}: {self.value}")

class test:
    """
    using list in another process
    """

    def __init__(self):
        manager = multiprocessing.Manager()
        self.list = manager.list()
        #value of item
        self.value = manager.Value

    def get_first_item_in_process(self):
        """
        get the first item in the list in another process
        """
        if self.list:
            return self.list[0]
        return None

    def remove_first_item_in_process(self):
        """
        remove the first item in the list in another process
        """
        if self.list:
            self.list.pop(0)

    def add_list(self, item):
        """
        add an item to the list
        """
        self.list.append(item)
    
    def process_start(self):
        """
        start the process in main process
        """
        _process = multiprocessing.Process(target=self.process_run)
        _process.start()
    
    def process_run(self):
        _item = self.get_first_item_in_process()
        self.change_item_in_process()
        time.sleep(2)
        self.remove_first_item_in_process()
    
    def change_item_in_process(self):
        """
        change the item in the list in another process
        """
        if isinstance(self.list[0], item):
            self.list[0].print_item()




    
if __name__ == "__main__":
    f = test()
    f.add_list(item("test", 1))
    f.add_list(1)
    f.add_list(item("test", 2))
    f.add_list(2)
    f.add_list(3)
    f.process_start()
    print(f.list)
    time.sleep(3)
    print(f.list)
    time.sleep(3)
    print(f.list)
    time.sleep(3)
    f.add_list(4)
    f.process_start()
    print(f.list)
    time.sleep(3)
    print(f.list)

