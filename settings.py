# -*- coding: utf-8 -*-

'''settings.py
Define global and environment-specific settings here.
'''
# there's a bug in datastructure so don't change the next two lines
BLOCK_TIME = 4.5
BLOCK_GO_N = 18

# set the two features we used for making the stimulus
shape = ['square', 'triangle', 'circle']
# texture = ['dot', 'solid', 'stripe']

# locate path of experiment specification related files
condition_path = './parameters/ConditionsSpecifications.csv'
trialheader_path = './parameters/TrialHeaders.csv'
trialspec_path = './parameters/TrialSpecifications.csv'
stimulus_dir = './stimuli/'

# column name of trial type names in TrialSpecifications.csv
trialspec_col = 'trial_type'

# task instruction
instr_txt = './instructions/exp_instr.txt'

# wait trigger screen
ready_txt = './instructions/wait_trigger.txt'


# MRI related settings
dummy_vol = 3
tr = 2
slice_per_vol = 60

from psychopy import logging
from src.fileIO import write_csv, create_headers
from src.datastructure.stimulus import stimulus_onefeat
from src.datastructure.datastructure import *
from src.datastructure import trialtype

# Base settings that apply to all environments.
# These settings can be overwritten by any of the
# environment settings.

BASE = {
    'test': False,
    'mouse_visible': False,
    'logging_level': logging.INFO
}


# Testing settings
TEST = {
    'test': True,
    'window_size': (1280, 720),
    'logging_level': logging.DEBUG
}

# Production settings
PRODUCTION = {
    'test': False,
    'logging_level': logging.EXP
}

# Laboratory setting
LAB = {
    'env': 'lab',  # Enviroment name
    'window_size': 'full_screen',
    'input_method': 'keyboard'
    }



# # Development environment settings. Used for testing,
# # outside of the MR room.
# DEV = {
#     'env': 'dev',  # Enviroment name
#     'window_size': (800, 600),
#     'button_box': None,  # No button box

#     # Number of runs
#     'n_runs': 1,

#     # Rating scale descriptions
#     'gaze_desc': "Left                   \
#                                         Right",
#     'self_desc': "Very Negative                   \
#                                         Very Positive",
#     'other_desc': "Very Negative                   \
#                                         Very Positive",
# }

MRI = {
    'env': 'mri',
    'window_size': 'full_screen',
    'input_method': 'serial',
}

# experiment specific vesion related setting
VER_A = {
        'rec_color': 'blue',
        'loc_color': 'red',
        'rec_keys': ['z', 'x'],
        'loc_keys': ['n', 'm'],
        'rec_keyans': ['yes', 'no'],
        'loc_keyans': ['left', 'right']
        }

VER_B = {
        'rec_color': 'red',
        'loc_color': 'blue',
        'rec_keys': ['n', 'm'],
        'loc_keys': ['z', 'x'],
        'rec_keyans': ['yes', 'no'],
        'loc_keyans': ['left', 'right']
        }

VER_A_MRI = {
            'rec_keys': ['1', '2'],
            'loc_keys': ['6', '7']
            }

VER_B_MRI = {
            'rec_keys': ['6', '7'],
            'loc_keys': ['1', '2']
            }

def get_trial_generator(block):
    '''
    return a trial generator and a list of data log headers
    '''
    # now define the generators
    # create experiment parameters
    parameters = experiment_parameters(
            block_length=BLOCK_TIME, block_go_n=BLOCK_GO_N, runs=1)
    parameters.load_conditions(condition_path)
    parameters.load_header(trialheader_path)

    # create trial finder
    find_trial = trial_finder(trialspec_path=trialspec_path, trialspec_col=trialspec_col)

    # create stimulus generators
    # stimulus_generator = stimulus_twofeat(feature1=shape, feature2=texture)
    stimulus_generator = stimulus_onefeat(feature=shape)
    # now build the trials
    builder = trial_builder()
    # build the trial generator
    trial_generator = builder.build(parameters, find_trial, stimulus_generator, block)

    return trial_generator, parameters.headers


def get_settings(env, ver, test=False):
    '''Return a dictionary of settings based on
    the specified environment, given by the parameter
    env. Can also specify whether or not to use testing settings.

    Include keypress counter balancing
    '''
    # Start with the base settings
    settings = BASE

    # display and key press counter balancing
    if ver == 'A':
        settings.update(VER_A)
    elif ver == 'B':
        settings.update(VER_B)
    else:
        raise ValueError, 'Version "{0}" not supported.'.format(ver)

    if env == 'lab':
        settings.update(LAB)
    # elif env == 'dev':
    #     settings.update(DEV)
    elif env == 'mri':
        settings.update(MRI)
        if ver == 'A':
            settings.update(VER_A_MRI)
        elif ver == 'B':
            settings.update(VER_B_MRI)
        else:
            raise ValueError, 'Version "{0}" not supported.'.format(ver)
    else:
        raise ValueError, 'Environment "{0}" not supported.'.format(env)

    # Update it with either the test or production settings

    if test:
        settings.update(TEST)
    else:
        settings.update(PRODUCTION)

    return settings

from src.datastructure.stimulus import tup2str

def parse_stimulus_name(trial):
    '''
    parse tuples to proper file names
    '''
    for key in trial.keys():
        if type(trial[key]) is tuple:
            trial[key] = tup2str(stimulus_dir, trial[key], '.png')
        elif 'stimPic' in key and type(trial[key]) is str:
            if trial[key] not in ['?', 'SWITCH']:
                trial[key] = stimulus_dir + trial[key] + '.png'
    return trial
