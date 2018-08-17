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
        self.duration = trial['fix_duration']
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
        self.duration = trial['stim_duration']

    def show(self, clock):
        self.text.draw()
        self.window.flip()
        start_trial = clock.getTime()
        core.wait(self.duration)

        # set the following so it's competeble to responese screen
        Resp = None
        KeyResp = None
        KeyPressTime = None
        respRT = None
        correct = None

        return start_trial, KeyResp, Resp, KeyPressTime, respRT, correct

class responsescreen(object):
    '''
    the screen for the memory task
    '''
    def __init__(self, window, version):
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

        self.version = version
        self.keylist = []
        self.keyans = []

    def set_trial(self, trial):
        self.duration = trial['stim_duration']
        self.ans = trial['Ans']
        # change color of self.line and self.dash base on go trial task
        if 'NoGo'in trial['TrialType']:
            self.line.fillColor = 'black'
            self.dash.fillColor = 'black'
        elif 'Recog' in trial['TrialType']:
            self.line.fillColor = self.version['rec_color']
            self.dash.fillColor = self.version['rec_color']
            self.keylist = self.version['rec_keys']
            self.keyans = self.version['rec_keyans']

        elif 'Back' in trial['TrialType']:
            self.line.fillColor = self.version['loc_color']
            self.dash.fillColor = self.version['loc_color']
            self.keylist = self.version['loc_keys']
            self.keyans = self.version['loc_keyans']

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
        Resp = None
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

            KeyResp, Resp, KeyPressTime = get_keyboard(
                    clock, self.keylist, self.keyans)

        # get reaction time and key press
        if not np.isnan(KeyPressTime):
            respRT = KeyPressTime - start_trial
        else:
            KeyResp, Resp = 'None', 'None'

        # get correct trials
        if self.ans == 'NA':
            correct = None
        elif self.ans == Resp:
            correct = 1
        else:
            correct = 0

        return start_trial, KeyResp, Resp, KeyPressTime, respRT, correct

class Question(object):
    '''
    collect mind wandering report
    '''
    def __init__(self, window, questions, color):
        '''Initialize a question stimulus.
        Args:
        window - The window object
        questions - a list of dictionaries
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.description = visual.TextStim(self.window, text=None, height=34,
        wrapWidth=1100, color=color, font=sans)
        self.scale_h = visual.TextStim(self.window, text=None, height=34,
        wrapWidth=1100, pos=[50,-50],color=color, font=sans)
        self.scale_l = visual.TextStim(self.window, text=None, height=34,
        wrapWidth=1100, pos=[-50,-50],color=color, font=sans)
        self.questions = questions
        self.rating = visual.RatingScale(self.window, low=1, high=10, markerStart=5,
                precision=10, tickMarks=[1, 10],
                leftKeys='1', rightKeys='2', acceptKeys='4')

    def set(self, trial):
        self.description.setText(trial['Item'])
        self.scale_h.setText(trial['Min_Scale'])
        self.scale_l.setText(trial['Max_Scale'])

    def show(self, clock):
        keyState=key.KeyStateHandler()
        self.window.winHandle.push_handlers(keyState)
        self.description.draw()
        self.scale_h.draw()
        self.scale_l.draw()
        self.rating.draw()
        self.window.flip()
        start_trial = clock.getTime()

        pos = self.rating.markerStart
        inc = 0.1

        while self.rating.noResponse:
            if event.getKeys(keyList=['escape']):
                print('user quit')
                core.quit()

            if keyState[key._1] is True:
                pos -= inc
            elif keyState[key._2] is True:
                pos += inc

            if pos > 9:
                pos = 9
            elif pos < 0:
                pos = 0

            self.rating.setMarkerPos(pos)
            self.description.draw()
            self.rating.draw()
            self.window.flip()

        score = self.rating.getRating()
        rt = self.rating.getRT()
        self.rating.reset()
        return start_trial, score, rt


def get_keyboard(timer, respkeylist, keyans):
    '''
    Get key board response
    '''
    Resp = None
    KeyResp = None
    KeyPressTime = np.nan
    keylist = ['escape'] + respkeylist

    for key, time in event.getKeys(keyList=keylist, timeStamped=timer):
        if key in ['escape']:
            quitEXP(True)
        else:
            KeyResp, KeyPressTime = key, time
    # get what the key press means
    if KeyResp:
        Resp = keyans[respkeylist.index(KeyResp)]
    return KeyResp, Resp, KeyPressTime

def quitEXP(endExpNow):
    if endExpNow:
        print 'user cancel'
        core.quit()

class instructions(object):
    '''
    show instruction and wait for trigger
    '''
    def __init__(self, window, settings, instruction_txt, ready_txt):
        self.window = window
        self.settings = settings
        self.env = settings['env']
        self.instruction_txt = load_instruction(instruction_txt)
        self.ready_txt = load_instruction(ready_txt)[0]

        self.display = visual.TextStim(
                window, text='default text', font=sans,
                name='instruction',
                pos=[-50,0], height=30, wrapWidth=1100,
                color='black',
                ) #object to display instructions

    def parse_inst(self):
        '''
        I hard coded the part with text needs changing.
        Will need to change this in the future
        '''
        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{COLOR_REC}', self.settings['rec_color'].upper())
        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{COLOR_LOC}', self.settings['loc_color'].upper())
        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{KEY_REC_0}', self.settings['rec_keys'][0].upper())
        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{KEY_REC_1}', self.settings['rec_keys'][1].upper())
        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{KEY_LOC_0}', self.settings['loc_keys'][0].upper())
        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{KEY_LOC_1}', self.settings['loc_keys'][1].upper())

        return self.instruction_txt

    def show(self):
        # get instruction
        self.parse_inst()
        for i, cur in enumerate(self.instruction_txt):
            self.display.setText(cur)
            self.display.draw()
            self.window.flip()
            if i==0:
                core.wait(uniform(1.3,1.75))
            elif self.env == 'mri':
                event.waitKeys(keyList=['1', '2', '3', '4'])
            else:
                event.waitKeys(keyList=['return'])

    def waitTrigger(self):
        # wait for trigger; or just wait
        self.display.setText(self.ready_txt)
        self.display.draw()
        self.window.flip()

        if self.env == 'lab':
            core.wait(uniform(1.3,1.75))
        elif self.env == 'mri':
            event.waitKeys(keyList=['5'])
        else: # not supported
            raise Exception('Unknown environment setting')

def subject_info(experiment_info):
    '''
    get subject information
    return a dictionary
    '''
    dlg_title = '{} subject details:'.format(experiment_info['Experiment'])
    infoDlg = gui.DlgFromDict(experiment_info, title=dlg_title)

    experiment_info['Date'] = data.getDateStr()

    file_root = ('_').join([experiment_info['Subject'], experiment_info['Run'],
                            experiment_info['Experiment'], experiment_info['Date']])

    experiment_info['DataFile'] = 'data' + os.path.sep + file_root + '.csv'
    experiment_info['LogFile'] = 'data' + os.path.sep + file_root + '.log'

    if experiment_info['Environment'] is 'mri':
        experiment_info['MRIFile'] = 'data' + os.path.sep + file_root + '_voltime.csv'

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

