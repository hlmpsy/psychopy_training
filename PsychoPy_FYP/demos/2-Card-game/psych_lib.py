from psychopy import visual, core, data, event, sound, gui

class screenHelper:
	"""Screen helper class which allows for things like creating a simple text display screen"""	

	def __init__(self,win,contText="Press any key to continue",textPos=[0,0],contPos=[0,-0.9],textSize=0.08):
		self.win = win
		self.text = visual.TextStim(win,alignVert="center",alignHoriz="center",height=textSize)
		self.cont = visual.TextStim(win,alignVert="center",alignHoriz="center",height=textSize)
		self.cont.setText(contText)
		self.cont.setPos(contPos)
		self.text.setPos(textPos)

	def showScreen(self, txt, keys=[], end=False, noContText=False):
		"""Show a screen to the user, pressing a key to move on or quit application"""
		self.text.setText(txt) # set text
		self.text.draw() # prepare to show it
		if noContText == False:
			self.cont.draw()
		self.win.flip() # actually show it

		mouse = event.Mouse()

		looper = True
		while looper:
			buttons = mouse.getPressed()
			if 1 in buttons or 2 in buttons or 3 in buttons:
				looper = False

			for key in event.getKeys():
				if key in ['escape','q']:
					core.quit()

	def showTimedScreen(self, txt, time=1):
		"""Show a timed screen to the user"""
		self.text.setText(txt) # set text
		self.text.draw() # prepare to show it
		self.win.flip() # actually show it
		
		core.wait(time)	


class userDialog:
	"""Helper for generating a user dialog to give to the user"""
	def __init__(self,dialog_data,expName="Experiment"):
		self.info = {}
		self.dialog_data = dialog_data
		self.expName = expName

	def callDialog(self):
		"""Fire up the dialog instance and return the data"""

		#Set up dialog data
	  	for item in self.dialog_data:
			self.info[item] = ''

		dlg = gui.DlgFromDict(dictionary=self.info, title=self.expName)
		if not dlg.OK:
			core.quit()
		#Tack on date
		self.info['dateStr'] = data.getDateStr() #will create str of current date/time

		return self.info
