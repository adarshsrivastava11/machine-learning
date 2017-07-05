import nltk
import re
import sys
import zmq
from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
from mappers.line_mapper import *
from mappers.bisector_mapper import *
import ConfigParser

config = ConfigParser.RawConfigParser()  
config.read('config.ini')
geomapper_port = config.get('devices', 'geomapper')
client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
coll_coordinates.drop()
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:"+geomapper_port)
username = sys.argv[1] #username should go here
socket.setsockopt(zmq.SUBSCRIBE, username)

           
while True:
    input_sentence = socket.recv()
    print input_sentence
    input_sentence = input_sentence.split('@')[1]
    command = input_sentence.split(',')[0]
    if command == "Line":
        point_pair = input_sentence.split(',')[1]
        point_pair = ''.join(point_pair)
        point_pair = point_pair.split(':')[1]
        length = input_sentence.split(',')[2]
        length = ''.join(length)
        length = length.split(':')[1]
        length = ''.join(length)
        length = length.split()[0]
        lineMapper(point_pair,length,username)
    if command == "Bisect":
        point_pair = input_sentence.split(',')[1]
        point_pair = ''.join(point_pair)
        point_pair = point_pair.split(':')[1]
        bisectorMapper(point_pair,50,username)
