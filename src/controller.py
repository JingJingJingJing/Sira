from multiprocessing.pool import ThreadPool
from threading import *
class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model

    def processInput(self, instance, string):
        # self.view.set_pwd_mode(instance)
        # import pdb; pdb.set_trace() 
        self.view.lock.acquire(True)
        '''pool = ThreadPool()
        res = pool.apply_async(self.view.request_input,("sample:", instance, self.view.lock))
        return_val = res.get()'''

        thread = Thread(target = self.view.request_input, args = ("sample:", instance, self.view.lock))
        thread.start()

        """你要做的事情"""

        self.view.lock.release()
        thread.join()

        #self.view.request_input("sample:", instance, self.view.lock)
        return [string, ">>>"]
        '''
        def request_input(self, s:str, instance, mutex):
        instance.insert_text("\n" + s)
        instance.protected_len = len(s)
        instance.pending_request = True
        '''