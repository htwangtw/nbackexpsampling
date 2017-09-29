# -*- coding: utf-8 -*-

'''
0.0.1

stimulus feature generator
'''

from random import shuffle, randint
from itertools import product

class stimulus_twofeat(object):
    '''
    double feature stimulus generator
    
    save features and genenrate stimuli pair

    feature1, feature2 : list, features of stimulus

    '''
    def __init__(self, feature1, feature2):
        self.feature1 = feature1
        self.feature2 = feature2

    def generate(self):
        '''
        generate a pair of stimuli with no shared feature

        '''
        shuffle(self.feature1)
        shuffle(self.feature2)
        item_left = (self.feature1[0], self.feature2[0])
        item_right = (self.feature1[1], self.feature2[1])

        yield [item_left, item_right]

class stimulus_twofeat_mix(object):
    '''
    double feature stimulus generator with mixed congurency
    The stimulis pair can share one feature or no feature.
    
    save features and genenrate stimuli pair

    feature1, feature2 : list, features of stimulus

    '''
    def __init__(self, feature1, feature2):
        self.feature1 = feature1
        self.feature2 = feature2
        self.stimuli = list(product(self.feature1, self.feature2))

    def generate(self):
        '''
        generate a pair of stimuli

        '''
        shuffle(self.stimuli)
        item_left = self.stimuli[0]
        item_right = self.stimuli[1]

        yield [item_left, item_right]

class stimulus_onefeat(object):
    '''
    single feature stimulus generator

    save features and genenrate stimuli
    feature1, feature2 : list, features of stimuli

    '''
    def __init__(self, feature):
        self.stimuli = feature

    def generate(self):
        '''
        generate a pair of stimuli with no shared features

        '''

        shuffle(self.stimuli)
        yield [self.stimuli[0], self.stimuli[1]]


def tup2str(dir_path, tuple_stim, filesuffix):
    '''
    trun tuple to a string (filename)
    the filename must look like: 
        feature1_feature2.png

    dir_path: str
        example: './stimulus/'
    
    tuple_stim: tuple
        stimulus, ('feature1', 'feature2')
    
    filesuffix: str
        expample '.png'

    return
        str, example: './stimulus/feature1_feature2.png'
    '''
    return dir_path + ('_').join(tuple_stim) + filesuffix
