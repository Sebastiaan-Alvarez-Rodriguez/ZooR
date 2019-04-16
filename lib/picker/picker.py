#!/usr/bin/env python
import random
import datetime
import lib.data.dataset as dataset

class Picker(object):
    """Object which pickes items from given dataset"""
    def __init__(self, in_dataset):
        now = datetime.datetime.now()
        seed = now.year+now.month+now.day+now.hour+now.minute+now.second++now.microsecond
        random.seed(seed)
        self.dataset = in_dataset

    # Ask user for size of sample
    def ask_samplesize(self):
        while True:
            print('How large do you want your sample (max)?')
            choice = input('')
            if len(choice) == 0 or not choice.isdigit():
                print('Please provide a number')
            else:
                return int(choice)

    # Pick items at random out of the list
    def pick(self, samplesize):
        result = []
        for num, element in enumerate(self.dataset, 1):
            if len(result) < samplesize:
                result.append(element)
            else:
                s = int(random.random() * num)
                if s < samplesize:
                    result[s] = element
            if num % 20000 == 0:
                print('Iterated over {0} candidates'.format(str(num)))
        return result