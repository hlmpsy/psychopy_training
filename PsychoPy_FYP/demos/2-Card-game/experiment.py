#!/usr/bin/env python2
from psychopy import visual, core, data, event, sound, gui
import numpy as np
#Import own custom set of libraries
from exp_core import *
from psych_lib import *

### CONFIGURATION AREA ###
experiment_name = "Pairs game"
welcome_text = 'Welcome to Part 2 of the Pairs game'
instruction_text = 'You will be presented with a grid of objects to try and pair up.\n\nPlease click onto an item and then try and pair it up.\n\nIf you manage to make a pairing, then this will reflect on the screen\n\nTry and complete as quickly as possible.'
thanks_text = 'Many thanks for your participation'
window_size = [1366,738]
full_screen = True
### END OF CONFIGURATION AREA ###

#User dialog and call
user_dialog = userDialog(dialog_data=["participant", "session"],expName=experiment_name)
userInfo = user_dialog.callDialog()

#Now set up window
myWin = visual.Window(window_size, allowGUI=True, fullscr=full_screen)

#Create a new screen helper instance
screen = screenHelper(win=myWin, textSize=0.08, contText="Click mouse button to continue")
newgame = game(win=myWin, info=userInfo)

### EXPERIMENT STRUCTURE ###

#Welcome
screen.showScreen(txt=welcome_text)

#Instructions
screen.showScreen(txt=instruction_text)

#Experiment (See excel file for data)
newgame.startGame()

#End
screen.showTimedScreen(txt=thanks_text,time=2)