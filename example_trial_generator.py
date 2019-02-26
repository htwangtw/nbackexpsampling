'''
This is an example of how to generate a trial list
all the modules have documentation to some extend
find them by typing ?modulename to the console

set working directory to the task folder before running this example

H.T. Wang
'''

# example 1: build your own
from src.fileIO import load_conditions_dict, write_csv, create_headers
from src.datastructure.stimulus import stimulus_onefeat, stimulus_ExpSample
from src.datastructure.datastructure import *
from src.datastructure import trial_library


# set the two features we used for making the stimulus
shape = ['square', 'triangle', 'circle']
questions, _ = load_conditions_dict('./stimuli/ES_questions.csv')

# load experience sampling quesitons

# locate path of experiment specification related files

# ConditionsSpecifications.csv:
#        original design
# ConditionsSpecifications_ES.csv:
#       0 back condition,
#       the experience sampling part has not been implemented yet
# condition_path = './parameters/ConditionsSpecifications.csv'
condition_path = './parameters/ConditionsSpecifications_ES.csv'

trialheader_path = './parameters/TrialHeaders.csv'
trialspec_path = './parameters/TrialSpecifications.csv'
stimulus_dir = './stimuli/'

# column name of trial type names in TrialSpecifications.csv
trialspec_col = 'trial_type'
block = None # accept values: '0', '1', None
# now define the generators
# create experiment parameters
# a 1.5 min block can have 6 catch trials max for a pure 0-/1-back task
# (block_length=3, block_go_n=6)
# a 12 min block can have 8 go-task trials and 8 experience sampling probes max
# (block_length=12, block_go_n=16)
# runs - minimum 1;
parameters = experiment_parameters(block_length=12, block_go_n=16, runs=1)
parameters.load_conditions(condition_path)
parameters.load_header(trialheader_path)


# create trial finder
find_trial = trial_finder(trialspec_path=trialspec_path, trialspec_col=trialspec_col)

# create stimulus generators
stimulus_generator = stimulus_onefeat(features=shape)
exp_sample_generator = stimulus_ExpSample(questions)

# now build the trials
builder = trial_builder()
# build the trial generator
trial_generator = builder.build(parameters, find_trial, stimulus_generator, exp_sample_generator, block)
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
    write_csv(fileName='example_run1.csv', list_headers=parameters.headers, thisTrial=trial)

# to get run two: (only if the setting is  on)
# trials = next(trial_generator)
# for trial in trials:
#     write_csv(fileName='example_run2.csv', list_headers=parameters.headers, thisTrial=trial)
