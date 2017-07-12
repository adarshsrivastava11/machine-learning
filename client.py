import zmq
import sys
import time
import re
import ConfigParser
from informers.circle_inform import *
from informers.line_inform import *

config = ConfigParser.RawConfigParser()  
config.read('config.ini')
client_port = config.get('devices', 'client')
line_server_port = config.get('server-client', 'line-server') 
circle_server_port = config.get('server-client', 'circle-server')
username = sys.argv[1]
context = zmq.Context()
sock_circle = context.socket(zmq.REQ)
sock_line = context.socket(zmq.REQ)
sock_geo_mapper = context.socket(zmq.PUB)
sock_geo_mapper.connect("tcp://127.0.0.1:"+client_port)
sock_line.connect("tcp://127.0.0.1:"+line_server_port)
sock_circle.connect("tcp://127.0.0.1:"+circle_server_port)


units = ["cm","mm","km","is","an","us","kg","of","at"]



prob = []

while True:

    input_sentence = raw_input()

    sock_line.send(input_sentence)
    max_output_line = sock_line.recv()
    max_output_line = eval(max_output_line)
    prob_line = float(max_output_line["prob"])
    prob.append(prob_line)
    print prob

    sock_circle.send(input_sentence)
    max_output_circle = sock_circle.recv()
    max_output_circle = eval(max_output_circle)
    prob_circle = float(max_output_circle["prob"])
    prob.append(prob_circle)
    print prob

    maximum = 0.0
    index = 0
    for i in range(0,len(prob)):
        if prob[i] >= maximum:
            maximum = prob[i]
            index = i
    prob = []
    time.sleep(0.5)
    if (index == 0):
        processed_dict_line = line_info(input_sentence,str(max_output_line))
        sock_geo_mapper.send("%s@%s" % (username, str(processed_dict_line)))
    if (index == 1):
        processed_dict_circle = circle_info(input_sentence,str(max_output_circle))
        sock_geo_mapper.send("%s@%s" % (username, str(processed_dict_circle)))
        print processed_dict_circle
        
       
       