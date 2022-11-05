from django.db import models

# teomporary model for user. need to change password and add more stuff to it
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)