from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
import subprocess
from taggit.managers import TaggableManager

class UserProfile(models.Model):
    user = models.OneToOneField(User)    

class Clipping(models.Model):
    html = models.TextField()
    title = models.CharField(max_length=200)
    tags = TaggableManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
