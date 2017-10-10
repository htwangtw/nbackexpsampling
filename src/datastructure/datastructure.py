# -*- coding: utf-8 -*-
'''
build the data structure for the experiment
To do: change the current 2-back setting to n-back
'''

import codecs
import csv
from random import randrange, shuffle, randint

from . import trialtype
from .trialtype import *
from ..fileIO import *


class experiment_parameters(object):
    '''
    save basic parameter, late pass to trial_builder

    block_length: float
        the length of a condition block

        default as 1.5 minutes

    block_catch_n: int
        the number of catch trials (of any kind) in a block

        default as 6
    
    runs: int
        the number of time to go through a set of conditions

    '''
    def __init__(self, block_length=1.5, block_catch_n=6, runs=1):
        self.block_length = block_length
        self.block_catch_n = block_catch_n
        self.blocks = []
        self.conditions = []
        self.headers = None
        self.runs = runs
    
    def create_counter(self):
        '''
        create a counter in seconds
        '''
        return self.block_length * 60
    
    def load_conditions(self, condition_path):
        '''
        
        load all the conditions for building a block

        condition_path
            path to the condition file
        '''
        
        conditions, _ = load_conditions_dict(condition_path)

        # conditions = []
        # with codecs.open(condition_path, 'r', encoding='utf8') as f:
        #     reader = csv.reader(f)
        #     for cond in reader:
        #         conditions.append(cond[0])
        self.conditions = conditions
    
    def load_header(self, trialheader_path):
        _, header = load_conditions_dict(trialheader_path)
        self.headers = header
   

class trial_finder(object):
    '''
    find and create trials accroding to the trial specification
    later pass to trial_bulder

    trialspec_path: a path to the trial specification file
    trialspec_col: the column name directing to the trial specification info

    '''
    def __init__(self, trialspec_path, trialspec_col):
        self.trialspec_path = trialspec_path
        self.trialspec_col = trialspec_col

    def get(self, trial_type):
        '''
        get the trial by keyword 'trial_type'
        only the supporting ones works!

        trial_type: str

        '''
        with codecs.open(self.trialspec_path, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            #loop through csv list
            for row in reader:
                # first convert strings to float
                for item in row.keys():
                    row[item] = str2float(row[item])

                # if current rows trial type is equal to input, print that row
                if trial_type == row[self.trialspec_col]:
                    trial_spec = row

                    trial_mod = getattr(trialtype, trial_type)
                    return trial_mod(trial_spec=trial_spec, lst_header=None)

                else:
                    pass


class trial_builder(object):
    '''
    build trials for each run
    need these - 
        experiment_parameters: obj
            store experiment parameter
        
        trial_finder: obj
            it finds a trial generator for you
        
        stimulus_generator: obj
            it generate stimulus pair  
    '''
    def __init__(self):
        self.trial_index = 0
        self.dict_trials = []
        self.last_trial = None
        self.init_trial_index = 0

    def initialise(self, counter):
        '''
        clean the buffer and reset counter 

        counter: int
            the legth of the block in second
        '''
        self.dict_trials = []
        self.counter = counter
        self.last_trial = None
        self.trial_index = self.init_trial_index

    def set_block_sequence(self, conditions, block=None):

        '''
        only support random sequence for now

        conditions: list
            a list of conditions

        return
            condition, shuffled: lst
        '''
	if None:
        	shuffle(conditions)
        return conditions

    def block_trials(self, trial_finder, block, trial_headers):
        
        '''
        trial_finder: object  
            it finds what type of trial you need based on a string

        block: str
            the name of the current block

        trial_headers: lst
            the trial headers
        
        return 
            objects
        '''

        trial_NoGo = trial_finder.get(trial_type='NoGo')
        trial_NoGo.lst_header = trial_headers

        trial_Go1 = trial_finder.get(trial_type=block['GoTrial_1'])
        trial_Go1.lst_header = trial_headers

        trial_Go2 = trial_finder.get(trial_type=block['GoTrial_2'])
        trial_Go2.lst_header = trial_headers
        
        trial_Go = [trial_Go1, trial_Go2]

        return trial_NoGo, trial_Go

    def get_n_NoGo(self, trial_NoGo):
        '''
        generate a random number of no-go trials

        trial_NoGo: object
            the no-go trial object. only this object contains the information for this

        retrun 
            int
        '''
        
        n_min = int(trial_NoGo.trial_spec['trial_n_min'])
        n_max = int(trial_NoGo.trial_spec['trial_n_max']) + 1

        return randrange(n_min, n_max, 1)

    def save_trial(self, cur_trial, block):
        '''
        save the trial to the temporary list

        cur_trial: dict
            a trial in dictionary form
        
        block: str
            the current block name

        '''
        cur_trial['Condition'] = block
        cur_trial['TrialIndex'] = self.trial_index
        self.trial_index += 1
        self.dict_trials.append(cur_trial)
        self.last_trial = cur_trial

    def build(self, experiment_parameters, trial_finder, stimulus_generator):
        '''
        now let's build the trial generator

        experiment_parameters: obj
            store experiment parameter
        
        trial_finder: obj
            it finds a trial generator for you
        
        stimulus_generator: obj
            it generate stimulus pair   

        '''
        for cur in range(experiment_parameters.runs):

            # shuffle the blocks
            blocks = self.set_block_sequence(experiment_parameters.conditions)
            # initialize the output storage and the counter
            run  = []
            counter = experiment_parameters.create_counter()

            for block in blocks:
                
                # initalize the block
                self.dict_trials = []
                self.counter = counter
                self.last_trial = None # n-back
                
                # store the trial index here, if need to regenerate this block, load from here
                self.init_trial_index = self.trial_index

                # get the specific go trials according to the block you are in 
                trial_NoGo, trial_Go = self.block_trials(trial_finder, block, experiment_parameters.headers)

                while self.counter != 0: # start counting
                    for i in range(experiment_parameters.block_catch_n):
                        # get no-go trial number
                        n_NoGo = self.get_n_NoGo(trial_NoGo)

                        # genenrate the no-go trials before the go trial occur
                        for j in range(n_NoGo):
                            cur_trial, t = next(trial_NoGo.generate_trial(stimulus_generator=stimulus_generator, last_trial=self.last_trial))
                            self.counter -= t
                            self.save_trial(cur_trial, block['Condition'])
                        # generate the go trial
                        # go trial: 1 feature or 2 feature?
                        idx = randint(0, 1)
                        cur_trial, t = next(trial_Go[idx].generate_trial(stimulus_generator=stimulus_generator, last_trial=self.last_trial)) # n-back
                        self.counter -= t
                        self.save_trial(cur_trial, block['Condition'])

                    # add 1~ 2 no-go trials and then a switch screen to end this block
                    for k in range(randrange(1, 3, 1)):
                        cur_trial, t = next(trial_NoGo.generate_trial(stimulus_generator=stimulus_generator, last_trial=self.last_trial))
                        self.counter -= t
                        self.save_trial(cur_trial, block['Condition'])
                    
                    cur_trial, t = next(trial_NoGo.generate_trial(stimulus_generator=stimulus_generator, last_trial=self.last_trial))
                    cur_trial['TrialType'] = 'Switch'
                    cur_trial['stimPicMid'] = 'SWITCH'
                    cur_trial['stimPicLeft'] = None 
                    cur_trial['stimPicRight'] = None 

                    self.save_trial(cur_trial, block)

                    if self.counter != 0:
                        # if this list of trials is not good for the block, restart
                        self.initialise(counter)

                    else:
                        # if it's good save this block to the run 
                        print 'save this block'
                        run += self.dict_trials
            yield run


                
def str2float(string):
    '''
    detect if the string can be converted to float.
    if so, return the converted result
    else, return the input string
    '''
    try:
        return float(string)
    except ValueError:
        return string
