import datetime
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User)    


class Clipping(models.Model):
    html = models.TextField()
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=200, unique=True, editable=False)
    tags = TaggableManager(blank=True)
    source_url = models.URLField(blank=True, null=True)
    text_only = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ['-date_modified']

    def save(self, *args, **kwargs):
        self.filename = slugify(self.title)[0:25]

        date = datetime.datetime.now()
        format = '%Y-%m-%dT%H-%M-%f'
        self.filename = self.filename + "_" + date.strftime(format)

        super(Clipping, self).save(*args, **kwargs)
