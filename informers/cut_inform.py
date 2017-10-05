def cut_info(input_sentence):
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