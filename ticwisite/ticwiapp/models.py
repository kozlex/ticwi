from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicCategory(models.Model):
        category        =       models.CharField(max_length=255)

        def __unicode__(self):
                return self.category



class GuiTic(models.Model):
        image           =       models.CharField(max_length=255)



class Course(models.Model):
	name		=	models.CharField(max_length=255)
	date		=	models.DateTimeField('course date')
	description	=	models.CharField(max_length=255)
	importance	=	models.IntegerField()
        user 		= 	models.ForeignKey(User)
	def __unicode__(self):
        	return self.name

course = property(lambda u: Course.objects.get_or_create(name=u)[0])

class Tic(models.Model):
	USER_TYPE = (
    	(1, 'Participant'),
    	(2, 'Presenter'),
  	)
        course          =       models.ForeignKey(Course)
        category        =       models.ForeignKey(TicCategory)
        gui_tic         =       models.ForeignKey(GuiTic)
        user_type	= 	models.CharField( max_length=1 , default="i", choices=USER_TYPE)
        dummy_name  	=       models.CharField(max_length=255)

class CourseProposed(models.Model):
	name		=	models.CharField(max_length=255)
	category	=	models.CharField(max_length=255)
	description	=	models.IntegerField()
	user		=	models.ForeignKey(User)

class InstitutionProfile(models.Model):
        name            =       models.CharField(max_length=255)
        description     =       models.CharField(max_length=255)
        member_since    =       models.DateTimeField()
        email           =       models.CharField(max_length=255)

#class Friend_institution(models.Model):
#	this_institution	=	models.ForeignKey(InstitutionProfile)
#	friend_institution	=	models.ForeignKey(InstitutionProfile)

class UserTic(models.Model):
	user		=	models.ForeignKey(User)
	tic		=	models.ForeignKey(Tic)
	tic_category	=	models.ForeignKey(TicCategory)

class WhoParticipate(models.Model):
	course		=	models.ForeignKey(Course)
	user		=	models.ForeignKey(User)
	approve_tic	=	models.IntegerField()

class WhoPresent(models.Model):
	course	 	=	models.ForeignKey(Course)
	presenter	=	models.ForeignKey(User)


class CourseComment(models.Model):
	ACCESS_CHOICES = (
 	   ('public', 'Public'),
 	   ('private', 'Private'),
	)
	READ_CHOICES = (
           ('yes', 'Yes'),
           ('no', 'No'),
        )

	first_name 	=	models.CharField(max_length=200)
	second_name 	= 	models.CharField(max_length=200)
	body 		= 	models.TextField()
	pub_date 	= 	models.DateTimeField('date published')
	access 		= 	models.CharField(max_length=10, default="private", choices=ACCESS_CHOICES)
	already_read	=	models.CharField(max_length=4, default="no", choices=READ_CHOICES)
	course 		= 	models.ForeignKey(Course)

class  Inbox(models.Model):
        user            =       models.ForeignKey(User)

class InboxMessage(models.Model):
        READ_CHOICES = (
           ('yes', 'Yes'),
           ('no', 'No'),
        )

        body            =       models.TextField()
        already_read    =       models.CharField(max_length=4, default="no", choices=READ_CHOICES)
	pub_date        =       models.DateTimeField('date published')
        sender		= 	models.ForeignKey(User, related_name='inboxmessage_sender') 
	receiver	=	models.ForeignKey(User, related_name='inboxmessage_receiver')                                         

	def __unicode__(self):
               return self.body
