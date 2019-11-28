import nltk
from nltk.stem.lancaster import LancasterStemmer
# import Rpi.GPIO as GPIO
stemmer = LancasterStemmer()

import speech_recognition as sr
import pyttsx3

import numpy
import tensorflow
import json
import tflearn
import random
import pickle

speech = sr.Recognizer()

try:
    engine = pyttsx3.init()

except ImportError:
    print('Requested driver is not found')

except RuntimeError:
    print('Driver failed to initialize')

engine.setProperty('voice', 'english')
engine.setProperty("rate", 150)


with open("/home/rahul/Documents/v2/json file/intents.json") as f:
	data = json.load(f)

try:
	# print(h)
	with open("data.pickle", "rb") as f:
		words, labels, training, output = pickle.load(f)
except:
	words = []
	labels = []
	docs_x = []
	docs_y = []

	for intent in data["intents"]:
		for pattern in intent['patterns']:
			wrds = nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(wrds)
			docs_y.append(intent['tag'])

		if intent['tag'] not in labels:
			labels.append(intent['tag'])
		#print(labels)

	words = [stemmer.stem(w.lower()) for w in words if w != '?']
	words = sorted(list(set(words)))

	labels = sorted(labels)

	training = []
	output = []

	out_empty = [0 for _ in range(len(labels))]

	for x, doc in enumerate(docs_x):
		bag = []

		wrds = [stemmer.stem(w) for w in doc]

		for w in words:
			if w in wrds:
				bag.append(1)
			else:
				bag.append(0)

		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1

		training.append(bag)
		output.append(output_row)

	training = numpy.array(training)
	output = numpy.array(output)
	with open("data.pickle", "wb") as f:
		pickle.dump((words, labels, training, output),f)


tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
	# print(h)
	model.load("model.tflearn")
except:
	model.fit(training, output, n_epoch=1000, batch_size=8, show_metric= True)
	model.save("model.tflearn")


def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[i] = 1

	return numpy.array(bag)


def read_voice_cmd():
	voice_text = ''
	with sr.Microphone() as source:
		audio = speech.listen(source)
	try:
		voice_text = speech.recognize_google(audio)

	except sr.RequestError:
		print('Network Error found')
		return ('None')
	except sr.UnknownValueError:
		error = "I am sorry, Please say again."
		return ('None')

	return voice_text


def train():
	question = []
	answer = []
	while True:
		print("Question Please")
		coversation = read_voice_cmd()
		if coversation != "quit" and coversation != 'None' :
			question.append(coversation)
			print(question)
		else:
			break
		print('Answer')
		coversation = read_voice_cmd()
		if coversation != "quit" and coversation != 'None':
			answer.append(coversation)
			print(answer)
		else:
			break

def chat():
	print("start talking to bot ")
	while True:
		inp = input("Enter the question")
		print(inp)
		if inp.lower() == "quit":
			break

		results = model.predict([bag_of_words(inp, words)])
		results_index = numpy.argmax(results)
		tag = labels[results_index]
		# print(results_index)
		# print(results)

		for tg in data["intents"]:
			if tg["tag"] == tag:
				responses = tg["responses"]

		reply = random.choice(responses)
		print(reply)
		engine.say(reply)
		engine.runAndWait()



if __name__ == '__main__':
	while True:
		mode = input("Enter the mode")
		if mode == "chat":
			chat()
		else:
			train()












