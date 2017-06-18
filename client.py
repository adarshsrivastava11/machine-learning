import zmq
import sys
import time
import json
import demjson
# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock_line = context.socket(zmq.REQ)
sock_line.connect("tcp://127.0.0.1:5000")
sock_circle = context.socket(zmq.REQ)
sock_circle.connect("tcp://127.0.0.1:5002")
# Send a "message" using the socket
input_sentence = raw_input()
sock_line.send(input_sentence)
max_output_line = sock_line.recv()
print max_output_line
sock_circle.send(input_sentence)
max_output_circle = sock_circle.recv()
print max_output_circle
