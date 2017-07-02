import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import nltk.data
from nltk.tokenize import word_tokenize
import re
import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5560")
topicfilter = "0"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

def Geometry(filteredTokens):
    units = ['cm','mm','m','km']
    if 'line' in filteredTokens:
        print "Line"
        lineHandler(filteredTokens,units)
        return "Line"
    if 'circle' in filteredTokens:
        print "Circle"
        return "Circle"
    if 'bisector' in filteredTokens or 'bisect' in filteredTokens:
        print "Bisector"
        lineHandler(filteredTokens,units)
        return "Bisector"

Coordinates_Points_Map = {}
# print bool(Coordinates_Points_Map)
# Coordinates_Points_Map.update({'A':{'x':0,'y':0}})
# print Coordinates_Points_Map['A']['x']
# def coordinatesHandler()
def lineMapper(points,length):
    print points
    print length
    if not length:
        length = ['0']
    length = ''.join(length)
   
    p1 = points[1].upper()
    p2 = points[2].upper()
    if bool(Coordinates_Points_Map) ==  False:
        Coordinates_Points_Map.update({p1:{'x':0,'y':0}})
    try:

        p2_x = float(Coordinates_Points_Map[p1]['x']) + float(length)
        p2_y = Coordinates_Points_Map[p1]['y']
    except KeyError:
        p2_x = float(Coordinates_Points_Map[p1]['x'])/2
        p2_y = 0
    else:
        Coordinates_Points_Map.update({p2:{'x':p2_x,'y':p2_y}})
        fo = open("draw_command.js", "a")
        fo.write("drawLine("+str(Coordinates_Points_Map[p1]['x'])+","+str(Coordinates_Points_Map[p1]['y'])+","+str(Coordinates_Points_Map[p2]['x'])+","+str(Coordinates_Points_Map[p2]['y'])+");");
        fo.write("drawText(\'"+str(p1)+"\',"+str(Coordinates_Points_Map[p1]['x'])+","+str(Coordinates_Points_Map[p1]['y'])+");")
        fo.write("drawText(\'"+str(p2)+"\',"+str(Coordinates_Points_Map[p2]['x'])+","+str(Coordinates_Points_Map[p2]['y'])+");")
        print Coordinates_Points_Map
def bisectorMapper(points,length):
    if not length:
        length = ['50']
    p1 = points[0].upper()
    p2 = points[1].upper()
    try:

        pb_x = (int(Coordinates_Points_Map[p1]['x'])+int(Coordinates_Points_Map[p2]['x']))/2
        pb_y = (int(Coordinates_Points_Map[p1]['y'])+int(Coordinates_Points_Map[p2]['y']))/2
        bisector_point = p1.lower()
        Coordinates_Points_Map.update({bisector_point:{'x':pb_x,'y':pb_y}})
    except KeyError:
        print "The line is yet not there"
    else:
        print Coordinates_Points_Map


def pointHandler(point,x,y):
    return 1

def lineHandler(filteredTokens,units):

    s = ' '.join(filteredTokens)
    length = re.findall(r'\d+', s)
    print length
    digits_removed = ''.join([i for i in s if not i.isdigit()])
    digits_removed = digits_removed.split(' ')
    
    for words in digits_removed:
        if len(words) == 2:
            if words not in units:
                print words
                if "bisector" in filteredTokens or "bisect" in filteredTokens:
                    bisectorMapper(words,length)
                else:
                    lineMapper(words,length)
                
def circleHandler_radius(filteredTokens):
    s = ' '.join(filteredTokens)
    radius = re.findall(r'\d+', s)
    print radius

def circleHandler_radius_endpoints(filteredTokens):
    return 1

def circleHandler_diameter_endpoints(filteredTokens):
    return 1

def circleHandler(filteredTokens,units):
    s = ' '.join(filteredTokens)
   
    digits_removed = ''.join([i for i in s if not i.isdigit()])
    digits_removed = digits_removed.split(' ')
    
    for words in digits_removed:
        if len(words) == 1:
            if words not in units:
                circleHandler_radius(filteredTokens)
                print words
        if len(words) == 2 and 'radius' in filteredTokens:
            if words not in units:
                circleHandler_radius_endpoints(filteredTokens)
                print words
        if len(words) == 2 and 'diameter' in filteredTokens:
            if words not in units:
                circleHandler_diameter_endpoints(filteredTokens)
                print words
           
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
        lineMapper(point_pair,length)