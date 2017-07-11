from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
coll_coordinates.drop()
def perpendicularMapper(points,length,user):
    if not length:
        length = ['50']
    p1 = points[0].upper()
    p2 = points[1].upper()
    try:
        get_point_1 = coll_coordinates.find_one({"point_name" : p1,"user":user})
        p1_x = get_point_1.get('point_x')
        p1_y = get_point_1.get('point_y')
        get_point_2 = coll_coordinates.find_one({"point_name" : p2,"user":user})
        p2_x = get_point_2.get('point_x')
        p2_y = get_point_2.get('point_y')
        pb_x = float(p1_x+p2_x)/2
        pb_y = float(p1_y+p2_y)/2
        bisector_point = p1.lower()
        coordinates_map = {
            "user" : user,
            "point_name" : "",
            "time_added" : datetime.now(),
        }
        coordinates_map["point_name"] = bisector_point
        coordinates_map["point_x"] = pb_x
        coordinates_map["point_y"] = pb_y
        insert_point = coll_coordinates.insert_one(coordinates_map)
        fo = open("drawing_module/draw_command.js", "a")
        fo.write("drawLine("+str(pb_x)+","+str(pb_y)+","+str(pb_x)+","+str(pb_y+length)+");");
        fo.write("drawLine("+str(pb_x)+","+str(pb_y)+","+str(pb_x)+","+str(pb_y-length)+");");
        fo.write("drawText(\'"+str(bisector_point)+"\',"+str(pb_x)+","+str(pb_y)+");")
        fo.close()
    except KeyError:
        print "The line is yet not there"
    else:
        cursor = coll_coordinates.find({})
        for document in cursor: 
            pprint(document)

