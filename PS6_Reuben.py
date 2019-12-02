#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 1
Use this template script to present one trial with your desired structure
@author: katherineduncan
"""
#%% Required set up 
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window 
# so that you can still see your console 
import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging

# global shutdown key for debugging!
event.globalKeys.add(key='q',func=core.quit)

# create a gui object
subgui = gui.Dlg()
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]

ouputFileName = 'data' + os.sep + 'sub' + subjID + '_sess' + sessNum + '_wordlistoutput.csv'

if os.path.isfile(ouputFileName) :
    sys.exit("data for this session already exists")

outVars = ['subj', 'trial', 'word', 'group', 'response', 'rt','actualonset','stimOn','stimDur']
out = pd.DataFrame(columns=outVars)


# open a white full screen window
win = visual.Window(size=[1024, 768], fullscr=True, allowGUI=False,
                    color=(0,0,0), units = 'height')

win.recordFrameIntervals = True
win.refreshThreshold = 1/60 + 0.004
logging.console.setLevel(logging.WARNING)

trialInfo = pd.read_csv("wordlist.csv")

instFile = 'Instructions.jpg'

fixation = visual.TextStim(win, text='+', height=.05)

corFeedback = visual.TextStim(win, text='Correct!', pos=(0,0), height=.05)
incFeedback = visual.TextStim(win, text='Wrong!', pos=(0,0), height=.05)

onset = trialInfo.onset.values # save original onset values
trialInfo = trialInfo.sample(frac=1)
trialInfo = trialInfo.reset_index()
trialInfo.loc[:,'onset'] = onset

# set number of trials
nTrials = len(trialInfo)

stimDur = 0.25
isiDur = 1
respDur = 2
fbDur = 1

# prepare image for display
instr = visual.ImageStim(win, image='Instructions.jpg', interpolate=True)

# draw image to window buffer
instr.draw()
# flip window to reveal image
event.clearEvents() # this clears any prior button presses
win.flip()

# don't do anything until a key is pressed
event.waitKeys()


expClock = core.Clock() # won't reset
trialClock = core.Clock() # will reset at the beginning of each trial
stimClock = core.Clock() # will reset when stim are presented
fbClock = core.Clock() # reset for each feedback interval
for thisTrial in np.arange(0,nTrials):

    trialClock.reset()

    # draw a fixation cross
    fixation.draw()
    win.flip()

    # prepare stimuli during fixation period
    thisWord = visual.TextStim(win, text=trialInfo.loc[thisTrial,'word'],
                                pos=(0,0))
    thisWord.draw()

    # wait until onset of current trial
    # note: timing is relative to experiment clock, not trial clock
    while trialClock.getTime() < isiDur:
        core.wait(.001)
    out.loc[thisTrial,'actualonset'] = expClock.getTime()

    # then present stimuli after fixation is done
    win.flip()
    stimClock.reset()
    # record when stimulus was presented
    out.loc[thisTrial, 'stimOn'] = expClock.getTime()

    while stimClock.getTime() < stimDur:
            thisWord.draw()
            win.flip()
    
    # stimulus finished, remove from display
    win.flip()
    
    # record when stimulus removed
    if np.isnan(out.loc[thisTrial,'stimDur']): 
        out.loc[thisTrial,'stimDur'] = expClock.getTime()-out.loc[thisTrial,'stimOn']
        
    # check for a key response
    trialResp = None
    trialRT = None
    event.clearEvents() # clear out key presses prior to trial
    keys = event.waitKeys(keyList=['f','j'],timeStamped=stimClock)
    if len(keys)>0: # if response made, collect response information
        trialResp = keys[0][0] # setting trialResp will end the while loop (i.e., end the trial) 
        trialRT = keys[0][1]
        
    # show feedback
    if trialResp=='f' and trialInfo.loc[thisTrial,'group']=='f':
        corFeedback.draw()
    elif trialResp=='j' and trialInfo.loc[thisTrial,'group']=='j':
        corFeedback.draw()
    else:
        incFeedback.draw()
    win.flip()
    fbClock.reset()
    while fbClock.getTime() < fbDur:
        core.wait(.001)

    # record trial prarameters
    out.loc[thisTrial,'word'] = trialInfo.loc[thisTrial,'word']
    out.loc[thisTrial,'group'] = trialInfo.loc[thisTrial,'group']
    out.loc[thisTrial,'trial'] = thisTrial + 1
    
    # save responses, if made
    if trialResp=='f' and trialInfo.loc[thisTrial,'group']=='f':
        out.loc[thisTrial, 'accuracy'] = '1'
    elif trialResp=='j' and trialInfo.loc[thisTrial,'group']=='j':
        out.loc[thisTrial, 'accuracy'] = '1'
    else:
        out.loc[thisTrial, 'accuracy'] = '0'
    
    if trialResp != None: 
        out.loc[thisTrial, 'response'] = trialResp
        out.loc[thisTrial, 'rt'] = trialRT


# finish experiment
fixation.draw()
win.flip()
core.wait(1)

# manage output
out['subj'] = subjID
out.to_csv(subjID + '_wordlistoutput.csv', index = False)

core.wait(3)

win.close()
core.quit()
