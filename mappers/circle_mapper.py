from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
coll_circles = db['circles']

def circleMapper(center,radius,user):
    circles_map = {
        "user":user,
        "time_added":datetime.now(),
    }
    center = center[0].upper()
    if (coll_coordinates.count({"user":user}) == 0):
        coordinates_map = {
            "user" : user,
            "point_name" : "",
            "time_added" : datetime.now(),
        }
        coordinates_map["point_name"] = center
        coordinates_map["point_x"] = 0.0
        coordinates_map["point_y"] = 0.0
        insert_point = coll_coordinates.insert_one(coordinates_map)

    
    get_point = coll_coordinates.find_one({"point_name" : center,"user" : user})
    p1_x = get_point.get('point_x')
    p1_y = get_point.get('point_y')
    circles_map["center"] = center
    circles_map["radius"] = radius
    insert_circle = coll_circles.insert_one(circles_map)
    fo = open("drawing_module/draw_command.js", "a")
    fo.write("drawCircle("+str(p1_x)+","+str(p1_y)+","+str(radius)+");");
    fo.write("drawText(\'"+str(center)+"\',"+str(p1_x)+","+str(p1_y)+");")
    fo.close()
    cursor = coll_coordinates.find({"user":user})
    for document in cursor: 
        pprint(document)