'''
This is an example of how to generate a trial list
all the modules have documentation to some extend
find them by typing ?modulename to the console

set working directory to the task folder before runing this example

H.T. Wang
'''

# example 1: build your own
from src.fileIO import write_csv, create_headers
from src.datastructure.stimulus import stimulus_onefeat
from src.datastructure.datastructure import *
from src.datastructure import trialtype


# set the two features we used for making the stimulus
shape = ['square', 'triangle', 'circle']

# locate path of experiment specification related files
condition_path = './parameters/ConditionsSpecifications.csv'
trialheader_path = './parameters/TrialHeaders.csv'
trialspec_path = './parameters/TrialSpecifications.csv'
stimulus_dir = './stimuli/'

# column name of trial type names in TrialSpecifications.csv
trialspec_col = 'trial_type'
block = '0'

# now define the generators
# create experiment parameters
# a 1.5 min block can have 6 catch trials max
parameters = experiment_parameters(block_length=4.5, block_go_n=18, runs=1)
parameters.load_conditions(condition_path)
parameters.load_header(trialheader_path)

# create trial finder
find_trial = trial_finder(trialspec_path=trialspec_path, trialspec_col=trialspec_col)

# create stimulus generators
stimulus_generator = stimulus_onefeat(feature=shape)
# now build the trials
builder = trial_builder()
# build the trial generator
trial_generator = builder.build(parameters, find_trial, stimulus_generator, block)
# use it like this  - it's a list of dictionaries
# I would just use these to save participant's output
trials = next(trial_generator)


# expamlpe 2: you can also import a wrap-around function for the above procedure
# or modify the parameters in the wraparound to make as above

# from settings import get_trial_generator
# build the trial generator and gaet the trials
# trial_generator =  get_trial_generator()
# trials = next(trial_generator)

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
     write_csv(fileName='../example.csv', list_headers=parameters.headers, thisTrial=trial)
