from django.shortcuts import render_to_response
from ticwiapp.models import Course, User, WhoPresent, WhoParticipate, Tic, CourseComment, Inbox, InboxMessage
from django.http import HttpResponse
from forms import CourseForm, TicForm, CourseCommentForm, InboxMessageForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict  
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from profilemanager.models import CustomUser
from django.db.models import Q
#from ticwiapp.forms import InboxMessageForm
import forms 

#from haystack.query import SearchQuerySet


class update_course(UpdateView):
    model = Course
    fields = ['name']
    template_name_suffix = '_update_form'
    #return HttpResponseRedirect('/ticwiapp/desktop')

def add_presenter_now(request, course_id=None, user_id=None):

    #If this presenter has not being added to the course, add it.
    current_presenter_obj = WhoPresent.objects.filter(course=course_id, presenter=user_id)
    if not current_presenter_obj:
         #Create an relational object with the course_id and presenter_id
         obj = WhoPresent(course_id = course_id , presenter_id = user_id)    
         obj.save()

    return HttpResponseRedirect('/ticwiapp/get_one_course/'+course_id)

def add_presenter(request, course_id=None):
    #Prepare presenters to add 
    args = {}
    args.update(csrf(request))
    #We are going to display just those users that are Participant or Presenter
    #TODO: Add a filter to just show those that have Presenter feature enabled
    args['presenters'] = CustomUser.objects.filter(user_type = "u")
    args['course_id'] = course_id 
    args['full_name'] = request.user.username
    return render_to_response('add_presenter.html', args) 

def add_participant_now(request, course_id=None, user_id=None):
    #If this participant has not being added to the course, add it.
    current_participant_obj= WhoParticipate.objects.filter(course=course_id, user=user_id)
    if not current_participant_obj:
         #Create an relational object with the course_id and presenter_id
         obj = WhoParticipate(course_id = course_id , user_id = user_id, approve_tic='0')
         obj.save()
    #TODO: else Warn the user???
    return HttpResponseRedirect('/ticwiapp/get_one_course/'+course_id)

def add_participant(request, course_id=None):
    #Prepare users to add 
    args = {}
    args.update(csrf(request))
    args['participants'] =  CustomUser.objects.filter(user_type = "u")
    args['course_id'] = course_id
    args['full_name'] = request.user.username
    return render_to_response('add_participant.html', args)

def remove_presenter(request, course_id=None, user_id=None):
    obj = WhoPresent.objects.get(course_id = course_id , presenter_id = user_id)
    obj.delete()
    return HttpResponseRedirect('/ticwiapp/get_one_course/'+course_id)


def remove_participant(request, course_id=None, user_id=None):
    obj = WhoParticipate.objects.get(course_id = course_id , user_id = user_id)
    obj.delete()
    return HttpResponseRedirect('/ticwiapp/get_one_course/'+course_id)


def delete_course(request, course_id=None):
    # Course is detected and is called to delete, 
    # TODO: perhaps it is needed a validation that instance exist and confirmation question! 
    obj = Course.objects.get(id=course_id)
    obj.delete()
    return HttpResponseRedirect('/ticwiapp/desktop')


def all_courses(request):
    #THIS MIGHT BE DEPRECATED, courses.html is included in desktop.html
    #Shows all courses available in a table
    #TODO: Show the list with certain number of items so if there are 1000 split 50 by 50

    #language = 'en-gb'
    #session_language = 'en-gb'

    #if 'lang' in request.COOKIES:
    #    language = request.COOKIES['lang']

    #if 'lang' in request.session:
    #    session_language = request.sessiond['lang']

    args = {}
    args.update(csrf(request))
    #Filter only those that belong to this user :)
    args['courses'] = Course.objects.filter( user = request.user )
    #Follow query gets all unread commentd from all courses
    args['unread_comments'] = CourseComment.objects.filter( course =  Course.objects.filter( user = request.user ), already_read="no" ).count
    # Follow query gets all Inbox unread messages
    args['inbox_messages'] = InboxMessage.objects.filter( receiver =  request.user , already_read="no" ).count
    args['user'] = request.user
    #args['language'] = language
    #args['session_language'] = session_language
    args['full_name'] = request.user.username
    return render_to_response('courses.html', args)

def get_one_course(request, course_id=None):
    # Prepares course information, collecting presenters, participants.
    #course_instance = Course.objects.get( id=course_id )
    who_present_obj = WhoPresent.objects.filter( course_id=course_id )
    #Developer tip: notice that is being used id__in, which gets all objects
    #that were result of who_present_instance query; if it is used id = who_present_instance
    # only the first object will be retrieved excluding all others
    # See:https://docs.djangoproject.com/en/dev/ref/models/querysets/#in
    #presenter_instance = User.objects.filter( id__in=who_present_instance.values('presenter') )

    who_participate_obj = WhoParticipate.objects.filter( course_id=course_id )
    #participant_instance = User.objects.filter( id__in=who_participate_instance.values('user') )

    #We can now say that the Institution has read all the comments by joining the course
    if request.user.user_type == "i":
        CourseComment.objects.filter(course = course_id).update(already_read = "yes")

    #Look for Participants Tic
    participant_tic_obj = Tic.objects.filter( course_id = course_id, user_type = "u")
    args = {}
    args.update(csrf(request))
    args['presenters'] = User.objects.filter( id__in=who_present_obj.values('presenter') ) #presenter_instance
    args['participants'] = User.objects.filter( id__in=who_participate_obj.values('user') ) #participant_instance
    args['course'] = Course.objects.get( id=course_id )
    args['participant_tic'] = Tic.objects.filter( course_id = course_id, user_type = "i")
    args['presenter_tic'] = Tic.objects.filter( course_id = course_id, user_type = "u")
    args['full_name'] = request.user.username
    return render_to_response('course.html',args)
                              
def create_course( request, course_id=None ):

    #Firstst of all we need to make user that non-institutions can't create courses
    if request.user.user_type == "u":
	return HttpResponseRedirect('/ticwiapp/desktop')
    #Prepares the information to update or create a new course.

    #if id:
    #    instance = get_object_or_404(Course, id=course_id)
    #    form = CourseForm(request.POST or None, instance=instance)
    #    if form.is_valid():
    #        form.update()
    #        return HttpResponseRedirect('/ticwiapp/get/')
    #    course = Course.objects.get(id=id)
    #    dictionary = model_to_dict(course, fields=[], exclude=[]) 
    #    form = forms.CourseForm(dictionary)
    #else:
    if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            a = form.save( commit = False )
            a.user = request.user
            a.save()

            return HttpResponseRedirect('/ticwiapp/desktop')
    else:
        form = CourseForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['full_name'] = request.user.username
    return render_to_response('create_course.html', args)

def add_tic( request, course_id, user_type=None ):
    if request.POST:
        form = TicForm(request.POST)
        if form.is_valid():
            a = form.save()

            return HttpResponseRedirect('/ticwiapp/get_one_course/'+course_id+"/"+user_type)
    else:
        form = TicForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['course_id'] = course_id
    args['user_type'] = user_type
    args['full_name'] = request.user.username
    return render_to_response('add_tic.html', args)

def delete_Tic(request, tic_id, course_id):
    # Tic is detected and is called to delete, 
    # TODO: perhaps it is needed a validation that instance exist and confirmation question! 
    obj = Tic.objects.get(id=tic_id)
    obj.delete()
    return HttpResponseRedirect('/ticwiapp/get_one_course/'+course_id)

def get_one_tic(request, tic_id=None):

    #Look for Participants Tic
    #tic_instance = Tic.objects.get( id = tic_id)
    args = {}
    args.update(csrf(request))
    args['tic'] =  Tic.objects.get( id = tic_id )
    args['full_name'] = request.user.username
    return render_to_response('tic.html',args)

def add_comment(request, course_id):
    a = Course.objects.get(id=course_id)

    if request.method == "POST":
        f = CourseCommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.pub_date = timezone.now()
            c.course = a
            c.save()
            return HttpResponseRedirect('/ticwiapp/get_one_course/%s' % course_id)
    else:
        f = CourseCommentForm()

    args = {}
    args.update(csrf(request))
    args['course'] = a
    args['form'] = f
    args['full_name'] = request.user.username
    return render_to_response('add_comment.html', args)

def change_course_comment_access(request, course_id, comment_id):
	c = CourseComment.objects.get(id=comment_id)
	if c.access == "private":
		c.access = "public"
	else:
		c.access = "private"
	
	c.save()
	return HttpResponseRedirect('/ticwiapp/get_one_course/%s' % course_id)

def search_user(request):
    #Prepare users to add 
    args = {}
    args.update(csrf(request))
    #TODO: Get all users but himself
    args['users'] =  CustomUser.objects.all()
    args['sender'] = request.user
    args['full_name'] = request.user.username
    return render_to_response('search_user.html', args)

def search_course(request):
    args = {}
    args.update(csrf(request))
    args['courses'] = Course.objects.filter()
    args['full_name'] = request.user.username
    return render_to_response('search_course.html', args)

def send_message(request, user_id, sender_id):
    sender_obj = User.objects.get(id = sender_id)
    receiver_obj = User.objects.get (id = user_id)

    if request.method == "POST":
        f = InboxMessageForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.pub_date = timezone.now()
	    c.sender = sender_obj
	    c.receiver = receiver_obj
            c.save()
            return HttpResponseRedirect('/ticwiapp/send_message/'+  user_id + "/" +  sender_id)
    else:
        f = InboxMessageForm()

    args = {}
    args.update(csrf(request))
    #follow query uses Q Objects to perform an AND / OR operation; geta all conversasion from user and sender
    args['messages'] = InboxMessage.objects.filter( Q(Q(sender_id = sender_obj) & Q(receiver_id = receiver_obj)) | Q(Q(sender_id = receiver_obj) & Q(receiver_id = sender_obj)) )
    #args['inbox'] = a   # course ??
    args['form'] = f
    args['user_id'] = user_id
    args['sender_id'] = sender_id
    #We can now say that messages  had been read  by  joining send message page
    InboxMessage.objects.filter(Q(sender_id = receiver_obj) & Q(receiver_id = sender_obj) ).update(already_read = "yes")
    args['full_name'] = request.user.username 
    return render_to_response('send_message.html', args)

def desktop(request):
    if request.user.user_type == "i":
        return HttpResponseRedirect('/ticwiapp/inst_desktop')
    else:
        return HttpResponseRedirect('/ticwiapp/user_desktop')

def inst_desktop(request):
    #TODO: Show the courses list with certain number of items so if there are 1000 split 50 by 50

    #language = 'en-gb'
    #session_language = 'en-gb'

    #if 'lang' in request.COOKIES:
    #    language = request.COOKIES['lang']

    #if 'lang' in request.session:
    #    session_language = request.sessiond['lang']

    args = {}
    args.update(csrf(request))
    #Filter only those that belong to this user :)
    args['courses'] = Course.objects.filter( user = request.user )
    #Follow query gets all unread commentd from all courses
    args['unread_comments'] = CourseComment.objects.filter( course =  Course.objects.filter( user = request.user ), already_read="no" ).count
    # Follow query gets all Inbox unread messages
    args['inbox_messages'] = InboxMessage.objects.filter( receiver =  request.user , already_read="no" ).count
    args['user'] = request.user
    args['full_name'] = request.user.username
    #args['language'] = language
    #args['session_language'] = session_language

    return render_to_response('inst_desktop.html',
                              args)

def user_desktop(request):
    #TODO: DESIGN user_desktop content
    args = {}
    args.update(csrf(request))
    args['full_name'] = request.user.username

    return render_to_response('user_desktop.html',
                              args)

