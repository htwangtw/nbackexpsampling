# -*- coding: utf-8 -*-

'''experiment.py
experiemnt stimulus here
'''
from psychopy import core, data, gui, visual, event, logging
import os
from src.fileIO import *
from random import uniform, shuffle

import numpy as np

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list

class Paradigm(object):
    '''
    Study paradigm
    '''
    def __init__(self, escape_key='esc', window_size=(1280, 720), color=0, *args, **kwargs):
        self.escape_key = escape_key
        self.trials = []
        self.stims = {}

        if window_size =='full_screen':
            self.window = visual.Window(fullscr=True, color=color, units='pix', *args, **kwargs)
        else:
            self.window = visual.Window(size=window_size, color=color, allowGUI=True, units='pix', *args, **kwargs)

class fixation_cross(object):
    '''
    fixation cross for this task
    '''
    def __init__(self, window, color='black'):
        self.window = window

        # i dont know how to draw a fixation cross
        self.line = visual.ShapeStim(self.window , name='verticle line',
            lineColor=None, fillColor=color,
            vertices=[(-2.5, 250), (-2.5,-250), (2.5,-250), (2.5, 250)])

        self.dash = visual.ShapeStim(self.window , name='dash line',
            lineColor=None, fillColor=color,
            vertices=[(-10, 2.5), (-10, -2.5), (10,-2.5), (10, 2.5)])

    def set_trial(self, trial):
        self.duration = trial['fixT']
        self.line.fillColor = 'black'
        self.dash.fillColor = 'black'

    def show(self, clock):
        self.line.draw()
        self.dash.draw()
        self.window.flip()
        start_trial = clock.getTime()
        core.wait(self.duration)
        return start_trial

class Text(object):
    '''
    show text in the middle of the screen
    such as 'switch'
    '''
    def __init__(self, window, text, color):
        '''Initialize a text stimulus.
        Args:
        window - The window object
        text - text to display
        duration - the duration the text will appear
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.text = visual.TextStim(self.window, text=text, height=34, wrapWidth=1100, color=color, font=sans)
        self.duration = None

    def set_trial(self, trial):
        self.duration = trial['stimT']

    def show(self, clock):
        self.text.draw()
        self.window.flip()
        start_trial = clock.getTime()
        core.wait(self.duration)

        # set the following so it's competeble to responese screen
        KeyResp = None
        KeyPressTime = None
        respRT = None
        correct = None

        return start_trial, KeyResp, KeyPressTime, respRT, correct

class responsescreen(object):
    '''
    the screen for the memory task
    '''
    def __init__(self, window, color):
        self.window = window
        self.line = visual.ShapeStim(self.window , name='verticle line',
                        lineColor=None, fillColor='black',
                        vertices=[(-2.5, 250), (-2.5,-250), (2.5,-250), (2.5,250)])

        self.dash = visual.ShapeStim(self.window , name='dash line',
                        lineColor=None, fillColor='black',
                        vertices=[(-10, 2.5), (-10, -2.5), (10,-2.5), (10, 2.5)])

        self.image_left = visual.ImageStim(self.window, name='stimPic-left',
                image=None, size=(250, 250), pos=(-250, 0))
        self.image_right = visual.ImageStim(self.window, name='stimPic-right',
                image=None, size=(250, 250), pos=(250, 0))
        self.image_mid = visual.ImageStim(self.window, name='stimPic-middle',
                image=None, size=(100, 100),pos=(0,0))

        self.quest_left = visual.TextStim(self.window, text='?',
                height=250, pos=(-250, 0), wrapWidth=500, color='black')
        self.quest_right = visual.TextStim(self.window, text='?',
                height=250, pos=(250, 0), wrapWidth=500, color='black')
        self.quest_mid = visual.TextStim(self.window, text='?',
                height=100,pos=(0,0), wrapWidth=200, color='white')

        self.present_left = None
        self.present_right = None
        self.present_mid = None

        self.color = color

    def set_trial(self, trial):
        self.duration = trial['stimT']
        self.ans = trial['Ans']
        # change color of self.line and self.dash base on go trial task
        if 'NoGo'in trial['TrialType']:
            self.line.fillColor = 'black'
            self.dash.fillColor = 'black'
        elif 'Back' in trial['TrialType']:
            self.line.fillColor = self.color[0]
            self.dash.fillColor = self.color[0]
        elif 'Recog' in trial['TrialType']:
            self.line.fillColor = self.color[1]
            self.dash.fillColor = self.color[1]

        if '?' == trial['stimPicLeft']:
            self.present_left = self.quest_left
            self.present_right = self.quest_right
        else:
            self.image_left.setImage(trial['stimPicLeft'])
            self.image_right.setImage(trial['stimPicRight'])
            self.present_left = self.image_left
            self.present_right = self.image_right

        if trial['stimPicMid'] is '?':
            self.present_mid = self.quest_mid

        elif trial['stimPicMid'] is None:
            self.present_mid = self.dash

        else:
            self.image_mid.setImage(trial['stimPicMid'])
            self.present_mid = self.image_mid

    def show(self, clock):
        event.clearEvents()

        correct = None
        respRT = np.nan
        KeyResp = None
        KeyPressTime = np.nan

        self.line.draw()
        self.present_left.draw()
        self.present_right.draw()
        self.present_mid.draw()
        self.window.flip()

        start_trial = clock.getTime()
        trial_clock = core.Clock()
        while KeyResp is None and (trial_clock.getTime() <= self.duration) :
            # get key press and then disappear
            self.line.draw()
            self.present_left.draw()
            self.present_right.draw()
            self.present_mid.draw()
            self.window.flip()

            KeyResp, KeyPressTime = get_keyboard(clock, ['left', 'right'])

        # get reaction time and key press
        if not np.isnan(KeyPressTime):
            respRT = KeyPressTime - start_trial
        else:
            KeyResp = 'None'

        # get correct trials
        if self.ans == KeyResp:
            correct = 1
        else:
            correct = 0

        return start_trial, KeyResp, KeyPressTime, respRT, correct

# class question(object):
#     '''
#     collect mind wandering report
#     '''

def get_keyboard(timer, respkeylist):
    '''
    Get key board response
    '''
    KeyResp = None
    KeyPressTime = np.nan
    keylist = ['escape'] + respkeylist

    for key, time in event.getKeys(keyList=keylist, timeStamped=timer):
        if key in ['escape']:
            quitEXP(True)
        else:
            KeyResp, KeyPressTime = key, time

    return KeyResp, KeyPressTime

def quitEXP(endExpNow):
    if endExpNow:
        print 'user cancel'
        core.quit()

def display_instructions(window, env, ver, txt_color='black', skip=False):
    def _instruction_ver(ver, text):
        # change instruction according to ver
        # ver A: red for location; blue for recognition
        # ver B: red for recognition; blue for location
        if ver is 'A':
            color = ['red', 'blue']
        else:
            color = ['blue', 'red']
        text = text.replace('{COLOUR_1}', color[0].upper()) # location
        text  = text.replace('{COLOUR_2}', color[1].upper())# recognition
        return color, text

    instruction_txt = load_instruction(os.path.abspath('./instructions/exp_instr.txt'))
    ready_txt = load_instruction(os.path.abspath('./instructions/wait_trigger.txt'))[0]
    instruction_stimuli = visual.TextStim(
        window, text='default text', font=sans,
        name='instruction',
        pos=[-50,0], height=30, wrapWidth=1100,
        color=txt_color,
        ) #object to display instructions
    color, instruction_txt[1] = _instruction_ver(ver, instruction_txt[1])
        #instructions screen
    if skip:
        pass
    else:
        for i, cur in enumerate(instruction_txt):
            instruction_stimuli.setText(cur)
            instruction_stimuli.draw()
            window.flip()
            if i==0:
                core.wait(uniform(1.3,1.75))
            else:
                # need a self-pace version for MR
                event.waitKeys(keyList=['return'])

    instruction_stimuli.setText(ready_txt)
    instruction_stimuli.draw()
    window.flip()

    if env == 'lab':
        core.wait(uniform(1.3,1.75))
    else:
        pass
        #need to update a fmri version (setting dev and mri)
    return color

def subject_info(experiment_info):
    '''
    get subject information
    return a dictionary
    '''
    dlg_title = '{} subject details:'.format(experiment_info['Experiment'])
    infoDlg = gui.DlgFromDict(experiment_info, title=dlg_title)

    experiment_info['Date'] = data.getDateStr()

    file_root = ('_').join([experiment_info['Subject'], experiment_info['Session'],
                            experiment_info['Experiment'], experiment_info['Date']])
    experiment_info['DataFile'] = 'data' + os.path.sep + file_root + '.csv'
    experiment_info['LogFile'] = 'data' + os.path.sep + file_root + '.log'

    if infoDlg.OK:
        return experiment_info
    else:
        core.quit()
        print 'User cancelled'

def event_logger(logging_level, LogFile):
    '''
    log events
    '''
    directory = os.path.dirname(LogFile)
    create_dir(directory)

    logging.console.setLevel(logging.WARNING)
    logging.LogFile(LogFile, level=logging_level)

def get_stim_screen(trial, switch_screen, stimulus_screen):
    '''
    trial: dict
        the current trial

    switch_screen: obj
        switch screen object

    stimulus_screen: obj
        stimulus screen object
    '''
    if trial['TrialType'] is 'Switch':
        switch_screen.set_trial(trial)
        return switch_screen
    else:
        stimulus_screen.set_trial(trial)
        return stimulus_screen

