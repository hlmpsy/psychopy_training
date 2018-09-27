from psychopy import visual, core, data, event, sound, gui
from psych_lib import *
import random
import numpy as np

class game:
	"""Main game object"""	

	def __init__(self,win,info):
		self.boards = [] #Empty board array
		self.reverseImage = 'images/card-back.png'
		self.win = win
		self.boardData = data.importConditions('expdata.xlsx') #Read in data file
		self.trials = data.TrialHandler(trialList=self.boardData, nReps=1, method="sequential")

		#Now create the experimentHandler
		self.thisExp = data.ExperimentHandler(
							name= "Card pair game", 
							version =1,
							extraInfo = info, #the info we created earlier
							dataFileName = "data/" + info['participant'] + "_" + info['session'] + "_part2_"+ info['dateStr']
						)		

	def startGame(self):
		"""Function to kick off the game"""

		#Get the trials/boards ready
		dataList = self.trials
		self.thisExp.addLoop(dataList) #Add list to the loop

		#Loop through each board from the excel data file
		for i, boardData in enumerate(dataList, start=0):

			#Build and create the game board
			gameBoard = board(win=self.win,gridSize=[boardData["gridWidth"], boardData["gridHeight"]],useCards=str(boardData["cardPack"]).split(','))

			#Start it
			rt = gameBoard.startBoard(i)

			#Add data to exp data
			self.trials.addData('rt', rt)

			#Tell the experiment handler that its on the next bit
			self.thisExp.nextEntry()



class board:
	"""The game board"""	

	def __init__(self,win,gridSize=[2,1],useCards=['1h','2c','3s','as','j'],showSpeed=0.5):
		self.complete = False
		self.useCards = useCards
		self.respClock = core.Clock()
		self.textScreen = screenHelper(win=win, textSize=0.08)
		self.showSpeed = showSpeed #This determines how long the card shows before returning back 
		self.myMouse = event.Mouse()
		self.win = win
		self.flipSpeed = 0.15
		self.x = gridSize[0]
		self.y = gridSize[1]
		self.heightAdjust = 1
		self.cardStack = [] #Empty stack to fill
		self.cardList = [] #Empty list of what cards we will show

		#If we have a silly grid size, then adjust so we always get 2 items
		if (self.x < 1 and self.y < 1):
			self.x = 2
			self.y = 1

		#Set up the grid ref distributions
		self.xrefs = self.getRefs(self.x)
		self.yrefs = self.getRefs(self.y)

		self.cards = int(gridSize[0]) * int(gridSize[1]) #amount of cards
		self.cardSize = self.sortCardSize() #Set the card size

		#Adjust to even amount of cards if required
		if self.cards % 2 != 0:
			self.cards = self.cards - 1

		#Set up the cards
		self.setUpCards()


	def sortCardSize(self):
		"""Work out a suitable size based on dimensions"""	

		widthSize = self.sortSizeDimension(self.xrefs)
		heightSize = self.sortSizeDimension(self.yrefs)

		#Fix size if proportions are disproportionate
		if heightSize > widthSize:
			heightSize = widthSize * 1.8

		if widthSize >= heightSize:
			widthSize = heightSize / 1.8

		return [widthSize,heightSize]


	def sortSizeDimension(self,refs):
		"""Work out a suitable size based on dimensions"""

		if len(refs) < 2:
			#Can only reliably calculate if there are two points of distance
			points = self.getRefs(2)
			return float((float(points[1]) - float(points[0]))/2)
		else:
			return float((float(refs[1]) - float(refs[0]))/2)


	def setUpCards(self):
		"""Take the card set given and pick 2 of the same from the deck and add to the stack"""

		totalCardsLeft = self.cards
		counter = 0
		stack = len(self.useCards)-1

		#Loop through whilst we still have cards left to add to the stack

		while totalCardsLeft > 0:
			#Append on two cards to the stack (pair)
			self.cardList.append(self.useCards[counter])
			self.cardList.append(self.useCards[counter])
			counter = counter + 1

			#Reset the counter if we've gone through the stack
			if counter > stack:
				counter = 0

			#Then decrement the count
			totalCardsLeft = totalCardsLeft - 2

		#Now shuffle the card set for display
		random.shuffle(self.cardList)

		#Now add the card objects to the stack
		counter = 0
		for x in range(0, len(self.xrefs)):
			for y in range(0, len(self.yrefs)):
				if(counter < self.cards):
					self.cardStack.append(pairItem(win=self.win,size=self.cardSize,pos=[self.xrefs[x],self.yrefs[y]],card=self.cardList[counter]))
					counter = counter + 1


	def redrawBoard(self):
		"""Loop through and draw any uncleared cards"""

		#Loop through X and Y and draw...
		for i, card in enumerate(self.cardStack):
			
			#Only draw the card if it isn't cleared
			if card.getCleared() == False:
				card.draw()

		self.win.flip()


	def getRefs(self,amount):
		"""Calculate distribution of ref points between two points"""

		portion = float(1)/float(amount)
		return np.linspace(-1+portion, 1-portion, num=amount)


	def startBoard(self,board=0):
		"""Start off the board level game"""

		#First show text screen to indicate what screen we're on
		self.textScreen.showTimedScreen("Starting board " + str(board+1), time=1)

		#Now show board itself
		self.redrawBoard()

		#Start the timer for reaction time
		self.respClock.reset()		

		#Initially set that we have no cards selected
		card_one = -1
		card_two = -1

		#IDEA - Would be nice to add a timer in for future games?  Is possible

		#Loop until the board is cleared!
		while self.complete == False: 

			#Loop through items and check if clicked, change state if required
			for i, card in enumerate(self.cardStack):
				if self.myMouse.isPressedIn(card) and card.getCleared() == False and card.getSelected() == False:
					
					#Would do an animation, but too slow with PsychoPy's win flip approach
					#Using another render would probably allow
					card.flipSelected()

					#Now flip the side to show back
					card.flipSide()	

					#Store the card pos in memory as one selected
					if card_one == -1:
						card_one = i
					else:
						card_two = i

					#Play the pick sound
					card_sound = sound.Sound(value="sounds/pick.wav")
					card_sound.play()

					#Now refresh the board again to reflect change
					self.redrawBoard()

					#Check if we have two selected
					if card_one > -1  and card_two > -1:

						#Check if they are a match
						if self.cardStack[card_one].getMainImage() == self.cardStack[card_two].getMainImage():
							
							#Show what was selected for a second
							core.wait(self.showSpeed)

							#Allow user to escape if required
							self.escapeCheck()

							#Show correct image and draw
							self.cardStack[card_one].setDisplay("correct")
							self.cardStack[card_two].setDisplay("correct")

							#Play the match sound
							card_sound = sound.Sound(value="sounds/match.wav")
							card_sound.play()

							#Time to update the board to reflect changes
							self.redrawBoard()

							#Now clear out those we had matched so they don't show
							self.cardStack[card_one].flipCleared()
							self.cardStack[card_two].flipCleared()

							#Now check if the board is clear .. we only check here
							#As we know that we've just made a match and there is opportunity that we've finished
							self.boardCleared()

							#Wait a sec to ensure the user sees the sequence for a moment
							core.wait(0.4)
						else:
							#If there was no match ... 

							#Show what was selected for a second
							core.wait(self.showSpeed)							

							#Allow user to escape if required
							self.escapeCheck()

							#Show incorrect image and draw
							self.cardStack[card_one].setDisplay("incorrect")
							self.cardStack[card_two].setDisplay("incorrect")

							#Play the nomatch sound
							card_sound = sound.Sound(value="sounds/nomatch.wav")
							card_sound.play()

							#Reflect things to the user so far
							self.redrawBoard()

							#Revert the two cards back
							self.cardStack[card_one].setSelected(False)
							self.cardStack[card_two].setSelected(False)
							self.cardStack[card_one].setDisplay("reverse")
							self.cardStack[card_two].setDisplay("reverse")

							#Wait a sec to show sequence
							core.wait(0.4)


						#Refresh again board to square one
						self.redrawBoard()	

						#Now reset the cards selected
						card_one = -1
						card_two = -1

					else:
						#wait for a split bit to stop double clicks
						core.wait(0.1)

			#See if the user wants out
			self.escapeCheck()

		#Record RT as we are at the end of the loop (board cleared)
		rt = self.respClock.getTime()

		#Now show a congrats screen!
		self.textScreen.showTimedScreen(txt="Well done! Board complete", time=1)

		#Better give back the RT to store later
		return rt


	def escapeCheck(self):
		"""Check if user wants out of the game"""
		for key in event.getKeys():
			if key in ['escape','q']:
				core.quit()

	def boardCleared(self):
		"""Check and see if we have cleared the board currently"""
		foundNotCleared = False

		for i, card in enumerate(self.cardStack):
			if card.getCleared() == False:
				foundNotCleared = True
				break #Break out of the loop early as we've found we still have uncleared items

		if foundNotCleared == False:
			self.complete = True




class pairItem:
	"""A pair object item - which can be a playing card for instance"""	
	
	def __init__(self,win,size,pos,card,reverseImage='images/card-back.png',correctImage='images/correct.png',incorrectImage='images/incorrect.png'):
		#self.stim = #image visual
		self.win = win
		self.mainImage = "images/" + self.setCardImage(card)
		self.reverseImage = reverseImage
		self.correctImage = correctImage
		self.incorrectImage = incorrectImage				
		self.display = "reverse"
		self.selected = False #Is this object selected?
		self.cleared = False #Is it a cleared item?
		self.displayObject = visual.ImageStim(win=self.win, name=str(card), image=reverseImage, mask=None,
                                    pos=pos, size=size, opacity=1)

	def setCardImage(self,card):
		"""Set the card image based on encoding and png.. assumes file exists"""	
		return str(card) + ".png"

	def draw(self):
		"""Determine what to draw for the card based on the display setting"""	
		if self.display == "reverse":
			#Set reverse image
			self.displayObject.setImage(self.reverseImage)
		elif self.display == "front":
			#Set card image
			self.displayObject.setImage(self.mainImage)
		elif self.display == "correct":
			#Set card image
			self.displayObject.setImage(self.correctImage)
		elif self.display == "incorrect":
			#Set card image
			self.displayObject.setImage(self.incorrectImage)

		#Then draw it
		self.displayObject.draw()

	#Bunch of flippers to flip states
	def flipSide(self):
		if self.getDisplay() == "reverse":
			self.setDisplay("front")
		else:
			self.setDisplay("reverse")


	def flipSelected(self):
		if self.getSelected() == True:
			self.setSelected(False)
		else:
			self.setSelected(True)

	def flipCleared(self):
		if self.getCleared() == True:
			self.setCleared(False)
		else:
			self.setCleared(True)	

	#Bunch of getters and setters
	def getMainImage(self):
		return self.mainImage

	def getDisplay(self):
		return self.display

	def setDisplay(self,display="reverse"):
		self.display = display

	def getSelected(self):
		return self.selected

	def setSelected(self, selected):
		self.selected = selected

	def getCleared(self):
		return self.cleared

	def setCleared(self,cleared):
		self.cleared = cleared

	def getHeight(self):
		sizeImage = self.displayObject.size
		return sizeImage[1]

	def setHeight(self,height):
		sizeImage = self.displayObject.size
		self.displayObject.setSize([sizeImage[0],height])

	def contains(self, objRef):
		"""Wrapper call for contains for ShapeStim"""			
		return self.displayObject.contains(objRef)