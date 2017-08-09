# -*- coding: utf-8 -*-
'''

trial design

all kind of supporting trial types

this one needs lot of cleaning
'''

from random import choice, shuffle, uniform
from ..fileIO import create_headers


class NoGo(object):
    '''
    generate a one back trial detail
    
    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):
        
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        t: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None
        
        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'],self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]
        dict_row['stimPicMid'] = None
        dict_row['Ans'] = 'None'

        yield dict_row, self.trial_spec['trial_t_total']
        


class ZeroBack(object):
    '''
    generate a zero back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'],self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]
        dict_row['stimPicMid'] = choice(item_list)

        if dict_row['stimPicMid'] == dict_row['stimPicLeft']:
            dict_row['Ans'] = 'left'
        else:
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']

    

class OneBack(object):
    '''
    generate a one back recall trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
        
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']

        dict_row['stimPicLeft'] = '?'
        dict_row['stimPicRight'] = '?'
        dict_row['stimPicMid'] = choice([last_trial['stimPicLeft'], last_trial['stimPicRight']])

        if dict_row['stimPicMid'] == last_trial['stimPicLeft']:
            dict_row['Ans'] = 'left'
        else:
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']

class Recognition(object):
    '''
    generate a one back recognition trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
        
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']

        # decide to preserve left or right
        for f1 in stimulus_generator.feature1: 
            if f1 not in [last_trial['stimPicLeft'][0], last_trial['stimPicRight'][0]]:
                distract_feature1 = f1
                
        for f2 in stimulus_generator.feature2: 
            if f2 not in [last_trial['stimPicLeft'][1], last_trial['stimPicRight'][1]]:
                distract_feature2 = f2
        distractor = (distract_feature1, distract_feature2)

        if choice(['left', 'right']) == 'left':
            dict_row['stimPicLeft'] = last_trial['stimPicLeft']
            dict_row['stimPicRight'] = distractor
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'left'

        else:
            dict_row['stimPicLeft'] = distractor
            dict_row['stimPicRight'] = last_trial['stimPicRight']
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'right'
           
        yield dict_row,self.trial_spec['trial_t_total']


class ZeroBack_feature(object):
    '''
    generate a zero back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
        
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]

        target_item = choice(item_list)
        target_feat = choice(target_item)

        # decide to preserve left or right
        # they all the items on screen can only share on feature
        if target_feat in stimulus_generator.feature1:
            for f2 in stimulus_generator.feature2: 
                if f2 not in [dict_row['stimPicLeft'][1], dict_row['stimPicRight'][1]]:
                    distract_feature2 = f2
            dict_row['stimPicMid'] = (target_feat, distract_feature2)
        
        else:
            for f1 in stimulus_generator.feature1: 
                if f1 not in [dict_row['stimPicLeft'][0], dict_row['stimPicRight'][0]]:
                    distract_feature1 = f1
            dict_row['stimPicMid'] = (distract_feature1, target_feat)

        if dict_row['stimPicLeft'] == target_item:
            dict_row['Ans'] = 'left'
        else:
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']

    

class OneBack_feature(object):
    '''
    generate a one back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
        
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']

        dict_row['stimPicLeft'] = '?'
        dict_row['stimPicRight'] = '?'

        target_item = choice([last_trial['stimPicLeft'], last_trial['stimPicRight']])
        target_feat = choice(target_item)
        # decide to preserve left or right

        if target_feat in stimulus_generator.feature1:
            for f2 in stimulus_generator.feature2: 
                if f2 not in [last_trial['stimPicLeft'][1], last_trial['stimPicRight'][1]]:
                    distract_feature2 = f2
            dict_row['stimPicMid'] = (target_feat, distract_feature2)
        
        else:
            for f1 in stimulus_generator.feature1: 
                if f1 not in [last_trial['stimPicLeft'][0], last_trial['stimPicRight'][0]]:
                    distract_feature1 = f1
            dict_row['stimPicMid'] = (distract_feature1, target_feat)

        if last_trial['stimPicLeft'] == target_item:
            dict_row['Ans'] = 'left'
        else:
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']


class Recognition_feature(object):
    '''
    generate a one back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
        
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted 

        output

        dict_row: dict
            a trail in dictionary 
        
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fixT'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stimT'] =self.trial_spec['trial_t_total'] - dict_row['fixT']
        # decide to preserve left or right
        for f1 in stimulus_generator.feature1: 
            if f1 not in [last_trial['stimPicLeft'][0], last_trial['stimPicRight'][0]]:
                distract_feature1 = f1
        for f2 in stimulus_generator.feature2: 
            if f2 not in [last_trial['stimPicLeft'][1], last_trial['stimPicRight'][1]]:
                distract_feature2 = f2
        distractor = (distract_feature1, distract_feature2)

        if choice(['left', 'right']) == 'left':

            target_item = last_trial['stimPicLeft']
            target_feat = choice(target_item)

            if target_feat in stimulus_generator.feature1:
                dict_row['stimPicLeft'] = (target_feat, last_trial['stimPicRight'][1])
            
            else:
                dict_row['stimPicLeft'] = (last_trial['stimPicRight'][0], target_feat)

            dict_row['stimPicRight'] = distractor
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'left'

        else:
            target_item = last_trial['stimPicRight']
            target_feat = choice(target_item)

            if target_feat in stimulus_generator.feature1:
                dict_row['stimPicRight'] = (target_feat, last_trial['stimPicLeft'][1])
            
            else:
                dict_row['stimPicRight'] = (last_trial['stimPicLeft'][0], target_feat)

            dict_row['stimPicLeft'] = distractor
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'right'
           
        yield dict_row,self.trial_spec['trial_t_total']