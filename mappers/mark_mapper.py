from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
db2 = client['commands']
draw_commands = db2['draw_commands']
def markMapper(point_name,point_x,point_y,user):
	coordinates_map = {
		"user" : user,
		"point_name" : "",
		"time_added" : datetime.now(),
	}

	coordinates_map["point_name"] = point_name
	coordinates_map["point_x"] = point_x
	coordinates_map["point_y"] = point_y
	insert_point = coll_coordinates.insert_one(coordinates_map)

	# fo = open("application-backend/app/assets/js/draw_command"+"_"+user+".js", "a")
	# fo.write("drawText(\'"+str(point_name)+"\',"+str(point_x)+","+str(point_y)+");")
	# fo.close()
	command = "drawText(\'"+str(point_name)+"\',"+str(point_x)+","+str(point_y)+");"
	draw_coommand_dict = {
        "username" : user,
        "command" : command,
        "executed" : False,
        "time_added" : datetime.now(),
    }

	insert_command = draw_commands.insert_one(draw_coommand_dict)
	cursor = coll_lines.find({"user":user})
	for document in cursor: 
		pprint(document)