import zmq
import sys
import time
import re

context = zmq.Context()
sock_circle = context.socket(zmq.REQ)
sock_line = context.socket(zmq.REQ)
sock_geo_mapper = context.socket(zmq.PAIR)
sock_geo_mapper.bind("tcp://127.0.0.1:5102")
sock_line.connect("tcp://127.0.0.1:5000")
sock_circle.connect("tcp://127.0.0.1:5002")
units = ["cm","mm","km","is","an","us","kg","of","at"]
def line_info(input_sentence,max_output_line):
    length = re.findall("\d+\.\d+", input_sentence)
    digits_removed = ''.join([i for i in input_sentence if not i.isdigit()])
    digits_removed = digits_removed.split(' ')
    for points_pairs in digits_removed:
        if len(points_pairs) == 2:
            if points_pairs not in units:
                points_pairs1 = ''.join(points_pairs)
    length = ''.join(length)
    processed_string = max_output_line.replace("$length",length)
    processed_string = processed_string.replace("$point_pair",points_pairs1)
    processed_string = processed_string.split('#')[0]
    processed_string = ''.join(processed_string)
    sock_geo_mapper.send(processed_string)
    return processed_string

prob = []
while True:
    input_sentence = raw_input()
    sock_line.send(input_sentence)
    max_output_line = sock_line.recv()
    prob_line = float(max_output_line.split('#')[1])
    prob.append(prob_line)
    sock_circle.send(input_sentence)
    max_output_circle = sock_circle.recv()
    prob_circle = float(max_output_circle.split('#')[1])
    prob.append(prob_circle)
    maximum = 0.0
    index = 0
    for i in range(0,len(prob)):
        if prob[i] >= maximum:
            maximum = prob[i]
            index = i
    prob = []
    time.sleep(0.5)
    if (index == 0):
        test = line_info(input_sentence,max_output_line)
        print test
       
       