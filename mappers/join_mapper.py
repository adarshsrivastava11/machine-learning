from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
import math
client = MongoClient()
db = client['geometry']
coll_coordinates = db['coordinates']
coll_lines = db['lines']
db2 = client['commands']
draw_commands = db2['draw_commands']
def joinMapper(first_point,second_point,user):
	lines_map = {
	    "user":user,
	    "time_added":datetime.now(),
	}
	try:
		get_point1 = coll_coordinates.find_one({"point_name" : first_point,"user":user})
		p1_x = get_point1.get('point_x')
		p1_y = get_point1.get('point_y')
		get_point2 = coll_coordinates.find_one({"point_name" : second_point,"user":user})
		p2_x = get_point2.get('point_x')
		p2_y = get_point2.get('point_y')

		lines_map["point_1"] = first_point
		lines_map["point_2"] = second_point
		lines_map["length"] = 0.0
		insert_line = coll_lines.insert_one(lines_map)

	# fo = open("application-backend/app/assets/js/draw_command"+"_"+user+".js", "a")
	# fo.write("drawLine("+str(p1_x)+","+str(p1_y)+","+str(p2_x)+","+str(p2_y)+");");
	# fo.close()
	except KeyError:
		print "The line is yet not there"
	else:
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