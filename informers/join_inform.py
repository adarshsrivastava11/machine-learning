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
