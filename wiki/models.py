from django.db import models

class Exercise(models.Model):
	id = models.CharField(max_length=30, primary_key=True)
	question = models.TextField()
	solution = models.TextField()

