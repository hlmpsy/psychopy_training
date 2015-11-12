#This will import a random integer function for our defined functions
from random import randint

#Fetch a text friendly month based on a month number

#"def" tells python that we are making a function
#A function is a piece of code that we can re-use many times
#and which performs a specific function for us
#"idx" is an ID variable which we pass to the function and use inside.
#In this case, it is a lookup ID refering to a month 1-12
def getMonth(idx):
	#First convert idx to an integer, just to be safe
	id_number = int(idx)

	#This is a list of text months, using what is called an "array"
	#Think of it as a pigeon hole that starts from 0 and goes up by 1
	#I.e. "January" is in pigeon hole reference 0, "December" is in 11.
	my_months=['January',
			   'February',
			   'March',
			   'April',
			   'May',
			   'June',
			   'July',
			   'August',
			   'September',
			   'October',
			   'November',
			   'December']
			   
	#Ensure we are using a valid range and return it from the list
	if (id_number >= 1) and (id_number <= 12):

		#Here we use the number to find the correct text date
		#We take 1 off the number passed, as our pigeon hole starts
		#at 0, so we adjust by 1
		#"return" is telling the function to give the value back to where 
		#it is called from.  Often it is assigned to a variable.
		return my_months[id_number-1]

    

#Pick a random month ID, which is from 1 to 12
#Notice that there is no value inside the () area, this means
#this function does not take parameters.
def getRandomMonthID():
    
    #randint is another Python function (which we imported from elsewhere)
    #It picks a random number between a range
    #, in this case from between 1 and 12
    #Return gives the result back to whatever called this function.
    return randint(1,12)
