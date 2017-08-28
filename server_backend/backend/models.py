from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	name = models.CharField(max_length=100)
	username = models.CharField(max_length=15)
	email = models.CharField(max_length=30)
	college = models.CharField(max_length=30)
	def __str__(self):
		return str(self.name)