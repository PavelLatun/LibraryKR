class Event:
    def __init__(self):
        self.__litener_list = []
        
    def add_listener(self, callback):
        self.__litener_list.append(callback)
        
    def remove_listener(self, callback):
        self.__litener_list.remove(callback)
        
    def remove_all_listener(self):
        self.__litener_list.clear()
        
    def invoke(self, *args):
        for callback in self.__litener_list:
            callback(*args)