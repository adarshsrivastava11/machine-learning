for a in range(ord('A'),ord('D')):
    for b in range(a,ord('G')):
    	if(chr(a) != chr(b)):
    		print("Bisect, line: $point_pair#Bisect line "+chr(a)+chr(b))
	        print("Bisect, line: $point_pair#Draw a bisector of line "+chr(a)+chr(b))
	        print("Bisect, line: $point_pair#Draw a perpendicular bisector of "+chr(a)+chr(b))
	        print("Perpendicular, line: $point_pair#Draw a perpendicular to "+chr(a)+chr(b))
	        print("Perpendicular, line: $point_pair#Draw a perpendicular of "+chr(a)+chr(b))
	        print("Perpendicular, line: $point_pair#Construct a perpendicular of "+chr(a)+chr(b))
	        print("Join, points: $point1+$point2#Join the point "+chr(a)+" and "+chr(b))
	        print("Join, points: $point1+$point2#Connect the point "+chr(a)+" and "+chr(b))