import multiprocessing

class Firepool(object):
    '''Object to balance workloads over multiple cores'''

    # Generic constructor
    def __init__(self):
        return
        
    # Execute multiprocess stage
    def fire(self, func, argarray):
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.starmap(func, argarray)