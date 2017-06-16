'''
This is an example of how to generate a trial list
all the modules have documentation to some extend
find them by typing ?modulename to the console

set working directory to the task folder before runing this example

H.T. Wang
'''
import os, sys
# add the source code folder to the system so this example can run
sys.path.append('./src')

# example 1: build your own
from fileIO import write_csv, create_headers
from trialstructure.stimulus import stimulus_twofeat
from trialstructure.experiment import *
from trialstructure import trialtype


# set the two features we used for making the stimulus
shape = ['square', 'triangle', 'circle']
texture = ['dot', 'solid', 'stripe']

# locate path of experiment specification related files
condition_path = './parameters/ConditionsSpecifications.csv'
trialheader_path = './parameters/TrialHeaders.csv'
trialspec_path = './parameters/TrialSpecifications.csv'
stimulus_dir = './stimuli/'

# column name of trial type names in TrialSpecifications.csv
trialspec_col = 'trial_type'

# now define the generators
# create experiment parameters
parameters = experiment_parameters(block_length=1.5, block_catch_n=6, runs=1)
parameters.load_conditions(condition_path)
parameters.load_header(trialheader_path)

# create trial finder
find_trial = trial_finder(trialspec_path=trialspec_path, trialspec_col=trialspec_col)

# create stimulus generators
stimulus_generator = stimulus_twofeat(feature1=shape, feature2=texture)

# now build the trials
builder = trial_builder()
# build the trial generator
trial_generator = builder.build(parameters, find_trial, stimulus_generator)
# use it like this  - it's a list of dictionaries
# I would just use these to save participant's output
trials = next(trial_generator)


# expamlpe 2: you can also import a wrap-around function for the above procedure 
# or modify the parameters in the wraparound to make as above

from settings import get_trial_generator
# build the trial generator and gaet the trials
trial_generator =  get_trial_generator()
trials = next(trial_generator)

# save it out; you can start from here to build an experiment
for trial in trials:
    # to save information, for example, kepress for the response
    # first, find the appropriate column name in './Stimuli/TrialHeaders.csv'
    # and the save information 
    # >> trial['keyResp'] = 'left'
    #
    # dictionary csv writer is way better than the normal text write 
    # when storing experiment data
    # 
    # the stimulus is saved as a tuple in the dictionar, use tup2str function in module stimulus
    # uncomment the following lines to compare theout put
    #
    from src.trialstructure.stimulus import tup2str
    for key in trial.keys():
        if type(trial[key]) is tuple:
            trial[key] = tup2str(stimulus_dir, trial[key], '.png')

    write_csv(fileName='./output/example_run2.csv', list_headers=parameters.headers, thisTrial=trial)
