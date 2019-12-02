#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
each cell in this script contains a different experiment ingredient.
it's not meant to be run from beginning to end but istead is a resource
that you can use to grab code snippets when building your own experiment

@author: katherineduncan
"""

#%% Required: import packages
"""
just like any python script, you'll want to import all your required packages
at the top of the script
this list isn't exhaustive, but contains many of the packages that you'll
likely need for an experiment
"""
import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging
# visual is needed to open a window and present visual stim
# core is needed for basic timing functions
# event is needed to get keypresses and mouse clicks
# gui lets you use a gui to collect info from experimenter

#%% Optional: collect info about session
"""
the built-in gui is a simple way to collect session information
you can include whatever fields you like! some experiments may not require this,
but usually you'll want subject info to save your data
"""
# create a gui object
subgui = gui.Dlg()

# add fields. the strings become the labels in the gui
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]

#%% Optional: prepare output
"""
once you have subject info, it's a good idea to make sure that you haven't
already run the subject! you can include a check up front
"""
ouputFileName = 'data' + os.sep + 'sub' + subjID + '_sess' + sessNum + '.csv'
if os.path.isfile(ouputFileName) :
    sys.exit("data for this session already exists")


#%% Required: set up your window
"""
your window is a box in which all stimuli are presented
it can be full screen (recomended for when your run a real experiment)
or it can be any size you like (can help when building an experiment)

see http://www.psychopy.org/api/visual/window.html for all options
"""

win = visual.Window(size=[800, 800], fullscr=False, allowGUI=False, color=(0,0,0), units = 'height')
# lots of optional parameters; these are just a few handy ones:
# size specifies how big the window is in pixels
# fullscr will override size if used
# allowGui determines whether a box with controls surrounds the screen
# color is in rgb from -1 to 1
# units will set default for how stimulus size is detfined
#    'height' will maintain aspect ratio while normalizing stim to screen size

# you can also include quality checks here to make sure that your screen refresh
# rate is what it should be. this is optional
win.recordFrameIntervals = True
win.refreshThreshold = 1/60 + 0.005
logging.console.setLevel(logging.WARNING)

# when you want to close the window use
win.close()

#%% Optional: presenting text
"""
here's how you draw text to your window
"""
# prepares text object
myText = visual.TextStim(win, text='Hello World', height=.05, color='black',
                           bold=True, pos=(0,.25))
# draws text to the window buffer
myText.draw()
# shows text
win.flip()

# prepare a longer statement on multiple lines
myText = visual.TextStim(win, text="""This is how you have one sentence.
                         And another underneath it.""", height=.05)
# draws text to the window buffer
myText.draw()
# shows text
win.flip()


#%% presenting an image
"""
here's how you draw an image from a file to your window
"""

# prepare image for display
instr = visual.ImageStim(win, image="instructions.jpeg", size=1, interpolate=True)
# be sure to use the full/relative path to the image location on your computer
# if you set your window units to "height" size=1 means full screen height
# setting interpolate to True will make images look nicer but could add time

# draw image to window buffer
instr.draw()
# flip window to reveal image
win.flip()

# prepare a smaller image on
face = visual.ImageStim(win, image="faces/1.jpg", pos = (.25,0))
# if you leave size at default, the image will be shown at it's native resolution
# this can save you processing time
# use pos to position the object on the screen

# draw image to window buffer
face.draw()
# flip window to reveal image
win.flip()


#%% recording a button press
"""
here's how you record a button press on your keyboard
"""

# waitKeys is a handy function that will run until a key is pressed
keys = event.waitKeys()
print(keys) # just for showing how it works!

# you can also set an time limit for the response period
keys = event.waitKeys(maxWait=2)
print(keys) # just for showing how it works!


# getKeys is like waitKeys, but it will only look for keys when it's called and
# then the script keeps going
# usually, you would use getKeys() in a while or for loop so it's called
# frequently

keys = []
while len(keys) < 1:
    keys = event.getKeys()

print(keys)

# you can also restrict which keys are valid by including a keyList
keys = event.waitKeys(keyList=['j','k'])  # now only j and k keys count
print(keys) # just for showing how it works!


# beware! if you press two keys at once both will be stored in a list!

# you can also record mouse clicks, but they are a little trickier
# see the mouse demo in the coder

#%% How to manage your timing
"""
there are several timing options
"""
# waits for time specified in seconds
core.wait(1)
# if you wait for long enough psychopy will let your computer do other things
# not super percise but okay if you don't need stimuli presented at exact times

# clocks are super handy -- they basically start stopwatches to tell you how
# long it's been since a particular event

trialClock = core.Clock()

# once you make a clock you can use it to ask how long it's been
timeInTrial = trialClock.getTime()


# you can also rest it at any point
trialClock.reset()
# it's faster to resset a clock than make a new one so this can make your
# code more efficient

#%% recording reaction times
"""
you can also use clocks to record RTs
"""

# after you
win.flip() # show something on the screen
trialClock.reset()
keys = event.waitKeys(timeStamped=trialClock)
print(keys)

# now waitKeys returns a list of lists
# to get the name of the key pressed use:
thisKey = keys[0][0]

# to get the reaction time use:
thisRT = keys[0][1]

# you can also make sure that only one key was pressed using
len(keys) == 1

# if its length is 0, then no keys were pressed
# if its lenght is >1, then more than one key was pressed

#%% recording text
"""
here's how you can record and dynamically update a typed response
"""
answer = ''
answerText = visual.TextStim(win, text=answer, height=.05)
win.flip()
done = 0
while done == 0:
    thisKey = event.waitKeys()

    if len(thisKey)==1: #only update if they press one key

        if thisKey[0] == 'backspace':
            if len(answer)>0:
                answer = answer[:-1]
        elif thisKey[0] == 'return':
            done = 1
            break
        else:
            answer += thisKey[0]

    answerText.text=answer
    answerText.draw()
    win.flip()

#%% working with rating scales
"""
psychopy has a built-in rating scale with many options
"""

# you can set the parameters at the beginning of an experiment
myRatingScale = visual.RatingScale(win, low=1, high=7, marker='triangle',
    tickMarks=[1,2,3,4,5,6,7],markerStart=None,markerColor='lightgrey')

# then you should reset your scale right before presentting it so RT is
# calcuated properly

myRatingScale.reset()  #reset rating scale right before drawing for RT
while myRatingScale.noResponse: # before the response is made
    myRatingScale.draw()
    win.flip()
#this loop will keep updating the rating scale as people make their decision

# you can then get their rating using this command:
thisRating = myRatingScale.getRating()

# and their decision time using this command:
myRatingScale.getRT()


#%% updating stimuli during a response window
"""
you can change your stimuli and check for responses at the same time
"""

stimDur = 0.5
respDur = 2
thisFace = visual.ImageStim(win, image='faces/1.jpg',)
thisFace.draw()
win.flip()
event.clearEvents() # clear any key presses that happened before response window
stimClock.reset() # reset stimulus and response window clocks
respClock.reset()
keys = [] # initialize response variable to empty list
while len(keys)==0 and respClock.getTime()<respDur:
    if stimClock.getTime()<stimDur: # keep displaying stimulus
        thisFace.draw()
        label.draw()
        win.flip()
    else: # stimulus duration finished, remove from display
        label.draw()
        win.flip()
    # check for a key response
    keys = event.getKeys(keyList=['j','k'],timeStamped=respClock)


#%% displaying feedback and tracking summary stats
"""
by checking responses within a trial, you can display feedback
"""

stimDur = 0.1
respDur = 2
fbDur = 1
corText = visual.TextStim(win, text='correct')
incText = visual.TextStim(win, text='incorrent')
thisFace = visual.ImageStim(win, image='faces/1.jpg',)
thisFace.draw()
win.flip()
event.clearEvents() # clear any key presses that happened before response window
stimClock.reset() # reset stimulus and response window clocks
respClock.reset()
keys = [] # initialize response variable to empty list
while len(keys)==0 and respClock.getTime()<respDur:
    if stimClock.getTime()<stimDur: # keep displaying stimulus
        thisFace.draw()
        label.draw()
        win.flip()
    else: # stimulus duration finished, remove from display
        label.draw()
        win.flip()
    # check for a key response
    keys = event.getKeys(keyList=['j','k'],timeStamped=respClock)
# check responses and display corresponding feedback
if keys[0][0]=='j':
    out.loc[thisTrial,'correct'] = 1 # save for summary at end: np.mean(out.correct)
    corText.draw()
elif keys[0][0]=='k':
    out.loc[thisTrial,'correct'] = 0
    incText.draw()
win.flip()


#%% use frame counting for timing
"""
more precise timing can be achieved with counts of frame draws to the screen
"""

stimFrameTotal = 3 # 3 frames x 16.7ms/frame = 50ms
thisFace = visual.ImageStim(win, image='faces/1.jpg',)
thisFace.draw()
win.flip()
# present stimuli for specified number of frames
for stimFrameN in range(stimFrameTotal-1):
    thisFace.draw()
    win.flip()
# remove stimulus
win.flip()


#%% adding timestamps to your data
"""
saving timestamps for trial events helps to confirm timing
"""

thisFace.draw()
while expClock.getTime()<trialOnset:
    core.wait(0.001)
win.flip()
# timestamp for onset of stimulus
out.loc[thisTrial,'stimOn'] = expClock.getTime()

while expClock.getTime()<trialOnset+stimDur:
    thisFace.draw()
    win.flip()
# duration of stimulus
out.loc[thisTrial,'stimDur'] = expClock.getTime()-out.loc[thisTrial,'stimOn']


#%% appending data to a csv file on every trial
"""
saving after each trial helps not lose data
"""

outputFileName = 'data/sub1_output.csv'
out = pd.DataFrame(columns=['trial','response','rt'])
out.to_csv(outputFileName,index=False)
stim = visual.TextStim(text='Press the j key!')
respClock = core.Clock()
for thisTrial in np.arange(nTrials):
    stim.draw() # display text
    win.flip()
    respClock.reset() # reset response clock
    keys = events.waitKeys(keyLists=['j'],timeStamped=respClock) # grab response
    win.flip() # display blank screen
    # store trial info
    out.loc[thisTrial,'trial'] = thisTrial
    out.loc[thisTrial,'response'] = keys[0][0]
    out.loc[thisTrial,'rt'] = keys[0][1]
    # append trial info to file, to_csv must be in append mode
    out.loc[[thisTrial]].to_csv(outputFileName,mode='a',header=False,index=False)
