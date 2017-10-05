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