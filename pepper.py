import speech_recognition as sr
import pyttsx3

import numpy
# import tensorflow
# import json
# import tflearn
import random
# import pickle

speech = sr.Recognizer()

try:
    engine = pyttsx3.init()

except ImportError:
    print('Requested driver is not found')

except RuntimeError:
    print('Driver failed to initialize')

engine.setProperty('voice', 'english')
engine.setProperty("rate", 150)



def read_voice_cmd():
	voice_text = ''
	with sr.Microphone() as source:
		audio = speech.listen(source)
	try:
		voice_text = speech.recognize_google(audio)

	except sr.RequestError:
		print('Network Error found')

	except sr.UnknownValueError:
		error = "I am sorry, Please say again."
		return error

	return voice_text

def getOrder():
	order = []
	speak_cmd("Please say the order")
	while True:
		item = input("Enter item name")
		if item == "thatsall":
			break
		else:
			order.append(item)
			print(order)	
	return order

def getConfirmation():
	return(input("confirm"))

def speak_cmd(cmd):
    engine.say(cmd)
    engine.runAndWait()

def chat():
	print("start talking to bot ")
	while True:
		speak_cmd("Are you ready to take order sir")
		inp = input("Enter the question")
		print(inp)

		if inp == "yes":
			speak_cmd("what would you like to have")
			list_of_items = getOrder()
			speak_cmd("your order is")
			for i in list_of_items:
				speak_cmd(i)
			speak_cmd("thank you for the order")
			speak_cmd("anything else")
			confirm = getConfirmation()
			if "yes" in confirm:
				speak_cmd("Thank you")
				break
			else:
				list_of_items.append(getOrder())
				for i in list_of_items:
					speak_cmd(i)
				speak_cmd("thank you for the order")
				break

		elif inp.lower() == "quit":
			break

		else:
			break
chat()














