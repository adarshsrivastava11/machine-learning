from random import randint
for a in range(ord('A'),ord('Z')):
	for b in range(ord(chr(a)),ord('M')):
		if(chr(a) != chr(b)):
			print("Line, line: $point_pair, length: $length cm#Construct a line "+chr(a)+chr(b)+" of length $length cm")
			print("Line, line: $point_pair, length: $length cm#Draw a line "+chr(a)+chr(b)+" of length $length cm")
			print("Line, line: $point_pair, length: $length cm#Draw a segment "+chr(a)+chr(b)+" of length $length cm")
			print("Line, line: $point_pair, length: $length cm#Construct "+chr(a)+chr(b)+" of length $length cm")
			print("Bisect, line: $point_pair#Bisect line "+chr(a)+chr(b))
			print("Bisect, line: $point_pair#Bisect line joining "+chr(a)+" and "+chr(b))
			print("Bisect, line: $point_pair#Divide line "+chr(a)+chr(b)+" in two equal parts")
			print("Cut, line: $point_pair, length: $length cm#Cut off "+chr(a)+chr(b)+" of length $length cm")
			print("Cut, line: $point_pair, length: $length cm#Cut "+chr(a)+chr(b)+" of length $length cm")
	