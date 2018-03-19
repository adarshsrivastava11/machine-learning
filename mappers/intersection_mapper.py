from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
coll_circles = db['circles']
db2 = client['commands']
draw_commands = db2['draw_commands']

def intersectionMapper(center,radius,user):
    circles_map = {
        "user":user,
        "time_added":datetime.now(),
    }
    try:
        center = center[0]
    except IndexError:
        center = 'A'
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

    try:
        get_point = coll_coordinates.find_one({"point_name" : center,"user" : user})
        p1_x = get_point.get('point_x')
        p1_y = get_point.get('point_y')
        print p1_x
        print p1_y
        circles_map["center"] = center
        circles_map["radius"] = radius
        g = -p1_x
        f = -p1_y
        c = g**2+f**2-radius**2
        circles_map["equation"] = "x**2 + y**2 + 2*"+str(g)" + 2*"+str(f)+" + "str(c)
        insert_circle = coll_circles.insert_one(circles_map)
    # fo = open("application-backend/app/assets/js/draw_command"+"_"+user+".js", "a")
    # fo.write("drawCircle("+str(p1_x)+","+str(p1_y)+","+str(radius)+");")
    # fo.write("drawText(\'"+str(center)+"\',"+str(p1_x)+","+str(p1_y)+");")
    # fo.close()
   

        command = "drawCircle("+str(p1_x)+","+str(p1_y)+","+str(radius)+");"+"drawText(\'"+str(center)+"\',"+str(p1_x)+","+str(p1_y)+");"
        draw_coommand_dict = {
            "username" : user,
            "command" : command,
            "executed" : False,
            "time_added" : datetime.now(),
        }
        insert_command = draw_commands.insert_one(draw_coommand_dict)
        cursor = coll_coordinates.find({"user":user})
        for document in cursor: 
            pprint(document)
            
    except AttributeError:
        print "Don't understand what you mean"