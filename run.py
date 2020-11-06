# -*- coding: utf-8 -*-

'''run.py
build the main program here
'''

import os
import sys

INFO = {
    'Experiment': 'nback_expsampling',  # compulsory
    'Subject': '001',  # compulsory
    'Run': '1',  # compulsory
    'Version': ['A', 'B'],  # counterbalance the fixation color
    'N-back': ['0', '1'],  # start the task with 1-back or 0-back
    'Environment': ['mri', 'lab']  # mri version can be tested on a normal stimuli delivery pc
    }

# MRI related settings
dummy_vol = 0
tr = 2
trigger_code = '5'

from settings import *
def run_experiment():
    from psychopy import core, event, logging, visual


    from src.experiment import (event_logger, Paradigm, fixation_cross,
                                Text, Question, get_stim_screen, responsescreen, instructions,
                                subject_info)
    from src.fileIO import read_only, write_csv
    # collect participant info
    experiment_info = subject_info(INFO)

    # set up enviroment variables and generators
    # set test to False when collecting participant
    settings = get_settings(
                    env=experiment_info['Environment'],
                    ver=experiment_info['Version'], test=False)

    trial_generator, headers = get_trial_generator(experiment_info['N-back'])

    # skip instruction expect run 1
    if experiment_info['Run'] == '1':
        skip_instruction = False
    else:
        skip_instruction = True


    # set log file
    event_logger(settings['logging_level'], experiment_info['LogFile'])

    # create experiment
    Experiment = Paradigm(escape_key='esc', color=0,
                          window_size=settings['window_size'])

    # hide mouse
    event.Mouse(visible=False)

    # put instruction on screen and get trigger
#    display_instructions(
#            window=Experiment.window,
#            settings=settings, skip=skip_instruction)

    instructions = instructions(
        window=Experiment.window, settings=settings,
        instruction_txt=instr_txt, ready_txt=ready_txt)

    # skip instruction except run 1
    if experiment_info['Run'] == '1':
        instructions.show()
    else:
        pass

    # create display screens
    fixation = fixation_cross(window=Experiment.window, color='black')
    stimulus = responsescreen(window=Experiment.window, version=settings)
    question = Question(window=Experiment.window, questions=None, color='white')
    switch = Text(window=Experiment.window, text='Switch', color='black')
    endtxt = open('./instructions/end_instr.txt', 'r').read().split('#\n')[0]
    end_msg = visual.TextStim(Experiment.window, text=endtxt, color='black',
                              height=34, wrapWidth=1100)

    # generate trials
    Experiment.trials = next(trial_generator)
    if experiment_info['Environment'] is 'mri':
        # wait trigger
        instructions.waitTrigger(trigger_code)
    # get a global clock
    timer = core.Clock()

    # dummy volumes
    if experiment_info['Environment'] is 'mri':
        fixation.set_trial({'fix_duration': tr * dummy_vol})
        t = fixation.show(timer)
        print('dummy volume start', t)

    # get a global clock
    timer = core.Clock()

    for trial in Experiment.trials:
        # parse tuples to proper file names
        trial = parse_stimulus_name(trial)
        # prepare fixation cross and stimulus display
        fixation.set_trial(trial)
        fix_t = fixation.show(timer)
        print(trial['TrialType'])

        if trial['TrialType'] == 'ExpSample':
            question.set(trial)
            start_stim, Resp, rt = question.show(timer)
        else:
            # show stimulus screen and catch response
            stim = get_stim_screen(trial, switch, stimulus)
            stim_t, KeyResp, Resp, KeyPressTime, respRT, correct = stim.show(timer)

        # post response fixation
        if respRT and trial['stim_duration'] - respRT > 0:
            fixation.duration = trial['stim_duration'] - respRT
            _ = fixation.show(timer)

        # dump information to trial
        trial['fixStart'] = fix_t
        trial['stimStart'] = stim_t
        trial['keyResp'] = KeyResp
        trial['resp'] = Resp
        trial['respCORR'] = correct
        trial['respRT'] = respRT
        trial['IDNO'] = experiment_info['Subject']
        trial['Run'] = experiment_info['Run']

        # write to csv
        write_csv(experiment_info['DataFile'], headers, trial)

        # clear answers
        KeyResp = None
        correct = None
        respRT = None

    # ending message
    end_msg.draw()
    Experiment.window.flip()
    event.waitKeys(keyList=['return'])

    logging.flush()
    # change output files to read only
    read_only(experiment_info['DataFile'])
    read_only(experiment_info['LogFile'])
    # quit
    Experiment.window.close()
    core.quit()

# now run this thing
if __name__ == "__main__":
    # set working directory as the location of this file
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    run_experiment()

