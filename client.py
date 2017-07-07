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
    # digits_removed = ''.join([i for i in input_sentence if not i.isdigit()])
    # digits_removed = digits_removed.split(' ')
    # for points_pairs in digits_removed:
    #     if len(points_pairs) == 2:
    #         if points_pairs not in units:
    #             points_pairs1 = ''.join(points_pairs)
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
    print max_output_circle
    radius = re.findall("\d+\.\d+", input_sentence) 
    center = re.findall(" [A-Z]", input_sentence) or re.findall("[A-Z] ", input_sentence)
    radius = ''.join(radius)
    center = ''.join(center)
    center = center.strip()
    max_output_circle = eval(max_output_circle)
    raw_string = max_output_circle["sentence"]
    processed_string = raw_string.replace("$radius",radius)
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
       
       