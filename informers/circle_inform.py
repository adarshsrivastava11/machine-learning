import re
def circle_info(input_sentence,max_output_circle):
    length_factor = re.findall("\d+\.\d+", input_sentence) 
    center = re.findall("(?!Draw)([A-Z])", input_sentence) or re.findall("[a-z]", input_sentence)
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
    
    return str(processed_dict)
