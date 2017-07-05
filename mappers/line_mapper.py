from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']

def lineMapper(points,length,user):
    
    p1 = points[0].upper()
    p2 = points[1].upper()
    if (coll_coordinates.count({"user":user}) == 0):
        coordinates_map = {
            "user" : user,
            "point_name" : "",
            "time_added" : datetime.now(),
        }
        coordinates_map["point_name"] = p1
        coordinates_map["point_x"] = 0.0
        coordinates_map["point_y"] = 0.0
        insert_point = coll_coordinates.insert_one(coordinates_map)

    
    get_point = coll_coordinates.find_one({"point_name" : p1,"user":user})
    p1_x = get_point.get('point_x')
    p1_y = get_point.get('point_y')
    p2_x = float(p1_x) + float(length)
    p2_y = p1_y
    coordinates_map = {
        "user" : user,
        "point_name" : "",
        "time_added" : datetime.now(),
    }
    coordinates_map["point_name"] = p2
    coordinates_map["point_x"] = p2_x
    coordinates_map["point_y"] = p2_y
    insert_point = coll_coordinates.insert_one(coordinates_map)
    # fo = open("draw_command.js", "a")
    # fo.write("drawLine("+str(Coordinates_Points_Map[p1]['x'])+","+str(Coordinates_Points_Map[p1]['y'])+","+str(Coordinates_Points_Map[p2]['x'])+","+str(Coordinates_Points_Map[p2]['y'])+");");
    # fo.write("drawText(\'"+str(p1)+"\',"+str(Coordinates_Points_Map[p1]['x'])+","+str(Coordinates_Points_Map[p1]['y'])+");")
    # fo.write("drawText(\'"+str(p2)+"\',"+str(Coordinates_Points_Map[p2]['x'])+","+str(Coordinates_Points_Map[p2]['y'])+");")
    # fo.close()
    cursor = coll_coordinates.find({"user":user})
    for document in cursor: 
        pprint(document)