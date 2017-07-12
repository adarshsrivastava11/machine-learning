import re

def join_info(input_sentence):
    points = re.findall("(?!Join|Point|Points)([A-Z])", input_sentence)
    first_point = points[0]
    second_point = points[1]
    print first_point
    print second_point
    processed_dict ={
        "command":"Join",
        "first_point":first_point,
        "second_point":second_point,
    }
    return str(processed_dict)

def mark_info(input_sentence):
    points = re.findall("(?!Mark|Point|Points)([A-Z])", input_sentence)
    print points[0]
    coordinates = re.findall("\d+\.\d+", input_sentence)
    coordinate_x = coordinates[0]
    coordinate_y = coordinates[1]
    print coordinate_x
    print coordinate_y
    processed_dict = {
        "command":"Mark",
        "point_name":points[0],
        "point_x":coordinate_x,
        "point_y":coordinate_y,
    }
    return str(processed_dict)

def line_info(input_sentence,max_output_line):
    if "Join" in input_sentence:
       join_output =  join_info(input_sentence)
       return join_output
    if "Mark" in input_sentence:
        mark_output = mark_info(input_sentence)
        return mark_output
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
