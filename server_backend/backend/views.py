
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from pymongo import MongoClient
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import time

client = MongoClient()
db = client['commands']
input_commands = db['new_commands']
output_commands = db['draw_commands']

def home(request):
	return render(request,'drawing.html')

@api_view(['GET'])
def student_collection(request):
	if request.method == 'GET':
		student = Student.objects.all()
		serializer = StudentSerializer(student,many=True)
		return Response(serializer.data)

@api_view(['GET'])
def student_element(request,username):
	if request.method == 'GET':
		try:
			student = Student.objects.get(username=username)
		except Student.DoesNotExist:
			return HttpResponse(status=404)
		serializer = StudentSerializer(student,many=False)
		return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
def add_command(request,username):
	command_map = {
		"username":username,
		"time_added":datetime.now(),
		"command":request.data.get('command'),
		"executed":False
	}
	print request.data.get("command")
	insert_command = input_commands.insert_one(command_map)
	return HttpResponse("Done!!")

@api_view(['GET'])
def get_output(request,username):
	time.sleep(1)
	output_command = output_commands.find_one_and_delete({"username": username})
	print output_command
	return HttpResponse(str(output_command["command"]))