from django.db import models


# Create your models here.

# poem class

class Poem(models.Model):
    title = models.CharField(max_length=200, default=None)
    score = models.IntegerField(default=0)
    description = models.TextField(default=None)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)
    author = models.CharField(max_length=50, default=None)
    date = models.DateTimeField(auto_now_add=True)


class Suggestion(models.Model):
    poem_id = models.ForeignKey('Poem',
                                on_delete=models.CASCADE)
    line = models.CharField(max_length=500, default=None)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

# login credentials
regular_user = {"username": "amber", "password": "regular"}
admin_user = {"username": "admin", "password": "admin"}
