import re
from mark_inform import *
from join_inform import *

def line_info(input_sentence,max_output_line):
    if "Join" in input_sentence:
       join_output =  join_info(input_sentence)
       return join_output
    if "Mark" in input_sentence:
        mark_output = mark_info(input_sentence)
        return mark_output
    if "Cut" in input_sentence:
        cut_output = cut_info(input_sentence)
        return cut_output
    else:
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
        return str(processed_dict)
