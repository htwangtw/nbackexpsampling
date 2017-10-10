# -*- coding: utf-8 -*-

'''run.py
build the main program here
'''

import os
import sys

from psychopy import core, event, logging, visual

from settings import *
from src.experiment import *
from src.fileIO import read_conly, write_csv

INFO = {
    'Experiment' : 'mindwandering_msc', # compulsory
    'Subject': 'R0001_001', # compulsory
    'Session': '1', # compulsory
    'Version': ['A', 'B'], # counterbalance the fixation cross
    'N-back': ['0', '1'], # start the task with 1-back or 0-back
    'Environment': ['lab', 'mri']
    }

# set up enviroment variables and generators
# set test to False when collecting participant
settings = get_settings(env=INFO['Environment'], test=True)

trial_generator, headers =  get_trial_generator(INFO['N-back'])

# collect participant info
experiment_info = subject_info(INFO)

# skip instruction expect run 1
if experiment_info['Session'] == '1':
    skip_instruction = False
else:
    skip_instruction = True

# now run this thing
if __name__ == "__main__":
    # set working directory as the location of this file
    _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
    os.chdir(_thisDir)

    # set log file
    event_logger(settings['logging_level'], experiment_info['LogFile'])

    # create experiment
    Experiment = Paradigm(escape_key='esc', color=0, window_size=settings['window_size'])

    # hide mouse
    event.Mouse(visible=False)

    # put instruction on screen
    display_instructions(window=Experiment.window, env=settings['env'], skip=skip_instruction)

    # create display screens
    fixation = fixation_cross(window=Experiment.window, color='black')
    stimulus = responsescreen(window=Experiment.window)
    switch = Text(window=Experiment.window, text='Switch', color='black')
    endtxt = open('./instructions/end_instr.txt', 'r').read().split('#\n')[0]
    end_msg = Text(window=Experiment.window, text=endtxt, color='black')

    # generate trials
    Experiment.trials= next(trial_generator)

    # get a global clock
    timer = core.Clock()

    for trial in Experiment.trials:
        # parse tuples to proper file names
        trial = parse_stimulus_name(trial)
        # prepare fixation cross and stimulus display
        fixation.set_trial(trial)
        stim = get_stim_screen(trial, switch, stimulus)

        # show fixation
        fix_t = fixation.show(timer)

        # show stimulus screen and catch response
        stim_t, KeyResp, KeyPressTime, respRT, correct = stim.show(timer)
        # post response fixation
        if respRT and trial['stimT'] - respRT > 0:
            fixation.duration = trial['stimT'] - respRT
            _ = fixation.show(timer)

        # dump information to trial
        trial['fixStart'] = fix_t
        trial['stimStart'] = stim_t
        trial['keyResp'] = KeyResp
        trial['respCORR'] = correct
        trial['respRT'] = respRT
        trial['IDNO'] = experiment_info['Subject']
        trial['Session'] = experiment_info['Session']

        # write to csv
        write_csv(experiment_info['DataFile'], headers, trial)

        #clear answers
        KeyResp = None
        correct = None
        respRT = None

    # ending message
    end_msg.duration = 2
    end_msg.show(timer)

    logging.flush()
    # change output files to read only
    read_conly(experiment_info['DataFile'])
    read_conly(experiment_info['LogFile'])
    # quit
    Experiment.window.close()
    core.quit()
