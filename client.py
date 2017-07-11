import zmq
import sys
import time
import re
import ConfigParser

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

def line_info(input_sentence,max_output_line):
    length = re.findall("\d+\.\d+", input_sentence) 
    points = re.findall("[A-Z][A-Z]", input_sentence)
    length = ''.join(length)
    points = ''.join(points)
    max_output_line = eval(max_output_line)
    raw_string = max_output_line["sentence"]
    processed_string = raw_string.replace("$length",length)
    processed_string = processed_string.replace("$point_pair",points)
    command = processed_string.split(',')[0]
    processed_dict = {
        "command":command,
        "end_points":points,
        "length":length,
    }
    sock_geo_mapper.send("%s@%s" % (username, str(processed_dict)))
    return processed_string

def circle_info(input_sentence,max_output_circle):
    length_factor = re.findall("\d+\.\d+", input_sentence) 
    center = re.findall(" [A-Z]", input_sentence) or re.findall("[A-Z] ", input_sentence) or re.findall(" [a-z]", input_sentence) or re.findall("[a-z] ", input_sentence) 
    length_factor = ''.join(length_factor)
    center = ''.join(center)
    center = center.strip()
    radius = 0.0
    max_output_circle = eval(max_output_circle)
    raw_string = max_output_circle["sentence"]
    if "$radius" in raw_string:
        radius = length_factor
        processed_string = raw_string.replace("$radius",length_factor)
    elif "$diameter" in raw_string:
        print "Found Diameter"
        radius = float(length_factor)/2
        processed_string = raw_string.replace("$diameter",length_factor)
   
    processed_string = processed_string.replace("$center",center)
    command = processed_string.split(',')[0]
    processed_dict = {
        "command":command,
        "center":center,
        "radius":radius,
    }
    sock_geo_mapper.send("%s@%s" % (username, str(processed_dict)))
    return processed_string

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
        extract_line = line_info(input_sentence,str(max_output_line))
        print extract_line
    if (index == 1):
        extract_circle = circle_info(input_sentence,str(max_output_circle))
        print extract_circle
       
       