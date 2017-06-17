import zmq
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
import re
import demjson

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5000")

# Run a simple "Echo" server
stemmer = LancasterStemmer()
# 3 classes of training data
training_data = []
training_data.append({"class":"Line, line: $point_pair, length: $length cm", "sentence":"Draw a line $point_pair of length $length cm"})
training_data.append({"class":"Line, line: $point_pair, length: $length cm", "sentence":"Construct a line $point_pair of length $length cm"})
training_data.append({"class":"Line, line: $point_pair, length: $length cm", "sentence":"Draw a line segment $point_pair of length $length cm"})
training_data.append({"class":"Line, line: $point_pair, length: $length cm", "sentence":"Draw $point_pair length equals $length cm"})

training_data.append({"class":"Line ,parent_line: $point_pair2, child_line: $point_pair1, length: 2*$length1 cm", "sentence":"Draw a line $point_pair1 such that it's length is twice of line $point_pair2"})
training_data.append({"class":"Line ,parent_line: $point_pair2, child_line: $point_pair1, length: 2*$length1 cm", "sentence":"Draw a line $point_pair1 such that it's length is twice of $point_pair2"})

training_data.append({"class":"Line, parent_line: $point_pair2, child_line: $point_pair1, length: 3*$length1 cm", "sentence":"Draw a line $point_pair1 such that it's length is thrice of line $point_pair2"})
training_data.append({"class":"Line, parent_line: $point_pair2, child_line: $point_pair1, length: 3*$length1 cm", "sentence":"Draw a line $point_pair1 such that it's length is thrice of $point_pair2"})

training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Bisect line $point_pair"})
training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Divide line AB in two parts"})
training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Draw a bisector of line $point_pair"})
training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Draw a perpindicular bisector of $point_pair"})
training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Divide the line $point_pair in two parts"})
training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Cut the line $point_pair in two equal halves"})
for a in range(ord('A'),ord('D')):
    for b in range(a,ord('G')):
        training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Bisect line "+chr(a)+chr(b)})
        training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Draw a bisector of line "+chr(a)+chr(b)})
        training_data.append({"class":"Bisect, line: $point_pair", "sentence":"Draw a perpindicular bisector of "+chr(a)+chr(b)})
        training_data.append({"class":"Perpendicular, line: $point_pair", "sentence":"Draw a perpindicular to "+chr(a)+chr(b)})
        training_data.append({"class":"Perpendicular, line: $point_pair", "sentence":"Draw a perpindicular of "+chr(a)+chr(b)})
        training_data.append({"class":"Perpendicular, line: $point_pair", "sentence":"Construct a perpindicular of "+chr(a)+chr(b)})
        training_data.append({"class":"Join, points: $point1+$point2", "sentence":"Join the point "+chr(a)+" and "+chr(b)})
        training_data.append({"class":"Join, points: $point1+$point2", "sentence":"Connect the point "+chr(a)+" and "+chr(b)})
        
       

training_data.append({"class":"Perpendicular, line: $point_pair", "sentence":"Draw a perpindicular to $point_pair"})
training_data.append({"class":"Perpendicular, line: $point_pair", "sentence":"Draw a perpindicular of $point_pair"})
training_data.append({"class":"Perpendicular, line: $point_pair", "sentence":"Construct a perpindicular of $point_pair"})

training_data.append({"class":"Join, points: $point_pair", "sentence":"Join $point_pair"})
training_data.append({"class":"Join, points: $point_pair", "sentence":"Connect $point_pair"})

training_data.append({"class":"Join, points: $point1+$point2", "sentence":"Join the point $point1 and $point2"})
training_data.append({"class":"Join, points: $point1+$point2", "sentence":"Connect the point $point1 and $point2"})

print ("%s sentences in training data" % len(training_data))
words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our training data
for pattern in training_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)
# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

print ("# words", len(words))
print ("# classes", len(classes))
# sample training/output
i = 0
w = documents[i][0]
print ([stemmer.stem(word.lower()) for word in w])
print (training[i])
print (output[i])
import numpy as np
import time

# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)
 
def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))



# probability threshold
ERROR_THRESHOLD = 0.2
# load our calculated synapse values
synapse_file = 'synapses_line.json' 
with open(synapse_file) as data_file: 
    synapse = json.load(data_file) 
    synapse_0 = np.asarray(synapse['synapse0']) 
    synapse_1 = np.asarray(synapse['synapse1'])

def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print ("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2
    # ANN and Gradient Descent code from https://iamtrask.github.io//2015/07/27/python-network-part2/

def classify(sentence, show_details=False):
    results = think(sentence, show_details)

    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
    results.sort(key=lambda x: x[1], reverse=True) 
    return_results =[[classes[r[0]],r[1]] for r in results]
    data_length = len(return_results)
    full_command = ""
    prob = ""
    for i in range(0,data_length):
        full_command = return_results[i][0]+"+"+full_command
        prob = str(return_results[i][1])+"*"+prob
    response_string = full_command+"#"+prob
    return response_string

units1 = ['cm','mm','km','to','of','by','is','it','an','in']
length=""
points_pairs1=""
while True:
    myinput = sock.recv()
    # length = re.findall(r'\d+',myinput)
    # digits_removed = ''.join([i for i in myinput if not i.isdigit()])
    # digits_removed = digits_removed.split(' ')
    # for points_pairs in digits_removed:
    #     if len(points_pairs) == 2:
    #         if points_pairs not in units1:
    #             points_pairs1 = ''.join(points_pairs)


    # length = ''.join(length)


    myoutput = classify(myinput)
    sock.send(myoutput)
    