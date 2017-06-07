
from django.db import models
from django.db.models import fields
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.timezone import activate

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    general=models.FloatField(default=0)
    sport=models.FloatField(default=0)
    business=models.FloatField(default=0)
    entertainment=models.FloatField(default=0)
    science_nature=models.FloatField(default=0)
    technology=models.FloatField(default=0)




    #other fields here

    def __str__(self):
          return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Source(models.Model):
    source_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    urlsToLogos_small = models.CharField(max_length=1000)
    urlsToLogos_medium = models.CharField(max_length=1000)
    urlsToLogos_large = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class News(models.Model):
    author = models.CharField(max_length=1000,null=True,blank=True)
    title = models.CharField(max_length=1000,null=True,blank=True)
    description = models.CharField(max_length=5000,null=True,blank=True)
    url = models.CharField(max_length=1000,null=True,blank=True)
    urlToImage = models.CharField(max_length=1000,null=True,blank=True)
    publishedDate = models.DateTimeField('Published Date',null=True,blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.title