from django.db import models
from django.contrib.auth.models import User


class GeneralUser(models.Model):
    user 	    =       models.ForeignKey(User) #models.OneToOneField(User)   
    name            =       models.CharField(max_length=255)

class UserProfile(User):
    second_name     =       models.CharField(max_length=255)
    birthday        =       models.DateTimeField()
    gender          =       models.IntegerField()
    picture         =       models.CharField(max_length=255)


class InstProfile(User):
    address         =       models.CharField(max_length=255)
    city            =       models.CharField(max_length=255)
    country         =       models.CharField(max_length=255)
    category        =       models.CharField(max_length=255)
    #type can be school, govuernamental, company, etc...
 
User.profile = property(lambda u: GeneralUser.objects.get_or_create(user=u)[0])
 
#Inst.profile = property(lambda u: InstProfile.objects.get_or_create(user=u)[0])
