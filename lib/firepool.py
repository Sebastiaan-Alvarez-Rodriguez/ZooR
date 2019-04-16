import multiprocessing

class Firepool(object):
    '''Object to balance workloads over multiple cores'''

    # Generic constructor
    def __init__(self):
        return

    # Ask how many cores to use for execution
    def ask_cores(self, max_cores=None):
        while True:
            print('You have '+str(multiprocessing.cpu_count())+' cores.')
            if max_cores:
                amount = input('How many cores can I use for processing? (max='+str(max_cores)+') ')
            else:
                amount = input('How many cores can I use for processing? ')
            if not amount.isdigit():
                print('Please enter a number')
            elif int(amount) < 1:
                print('I need at least 1 core')
            elif int(amount) > multiprocessing.cpu_count():
                print('You do not have '+amount+' cores')
            elif max_cores and int(amount) > max_cores:
                print('Please do not specify more than '+str(max_cores)+' cores')
            else:
                return int(amount)

    # Execute multiprocess stage
    def fire(self, func, argarray, processes=None):
        if processes==None:
            cores = self.ask_cores()
        else:
            cores = processes

        with multiprocessing.Pool(processes=cores) as pool:
            pool.starmap(func, argarray)