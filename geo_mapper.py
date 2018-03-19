import nltk
import re
import sys
import zmq
from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
from mappers.line_mapper import *
from mappers.bisector_mapper import *
from mappers.circle_mapper import *
from mappers.perpendicular_mapper import *
from mappers.join_mapper import *
from mappers.mark_mapper import *
import ConfigParser

config = ConfigParser.RawConfigParser()  
config.read('config.ini')
geomapper_port = config.get('devices', 'geomapper')
client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
coll_circles = db['circles']
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:"+geomapper_port)
username = sys.argv[1] #username should go here
socket.setsockopt(zmq.SUBSCRIBE, username)
coll_coordinates.remove({"user":username})
coll_lines.remove({"user":username})
coll_circles.remove({"user":username})

print "Geo Mapper Started"
       
while True:
    input_sentence = socket.recv()
    print input_sentence
    input_sentence = input_sentence.split('@')[1]
    input_sentence = eval(input_sentence)
    command = input_sentence["command"]
    print command
    if command == "Line":
        print "Line Excuted"
        point_pair = input_sentence["end_points"]
        print point_pair
        length = input_sentence["length"]
        print length
        lineMapper(point_pair,length,username)
    if command == "Cut":
        point_pair = input_sentence["end_points"]
        length = input_sentence["length"]
        lineMapper(point_pair,length,username)
    if command == "Bisect":
        point_pair = input_sentence["end_points"]
        bisectorMapper(point_pair,30,username)
    if command == "Perpendicular":
        point_pair = input_sentence["end_points"]
        perpendicularMapper(point_pair,30,username) 
    if command == "Circle":
        center = input_sentence["center"]
        radius = input_sentence["radius"]
        circleMapper(center,radius,username)
    if command == "Join":
        first_point = input_sentence["first_point"]
        second_point = input_sentence["second_point"]
        joinMapper(first_point,second_point,username)
    if command == "Mark":
        point_name = input_sentence["point_name"]
        point_x = input_sentence["point_x"]
        point_y = input_sentence["point_y"]
        markMapper(point_name,point_x,point_y,username)
