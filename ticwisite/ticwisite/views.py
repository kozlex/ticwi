from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from ticwiapp.models import Course, Inbox
from profilemanager.auth_backends import CustomUserModelBackend
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from profilemanager.models import CustomUser
import logging


logr = logging.getLogger(__name__)

def go_home(request):
    #This only verifies if user is authenticated to send to desktop or to login page
    if request.user.is_authenticated():
         return HttpResponseRedirect('/ticwiapp/desktop')
    else:
         return HttpResponseRedirect('/accounts/login')

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    #This is called during login and authenticates a login user
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    #It is granted that email is unique at Registration Form
    #Also is granted that username is unique by its email
    username = CustomUser.objects.filter(email = email).values('username')
    # Follow also works, it is only that we are getting the username in plain single text
    # like 613ef953ea32f6d2fc078b1928db02 instead of  [{'username': u'613ef953ea32f6d2fc078b1928db02'}]
    #username =  list(CustomUser.objects.filter(email = email).values_list('username', flat=True))[0]
    user = auth.authenticate(username=username, password=password)

    #If user is authenticated then we can call to desktop
    if user is not None:
        auth.login(request, user)
        args = {}
        args.update(csrf(request))
	args['courses'] = Course.objects.all()
        #TODO: Previous should get only those courses that belong to this account
        return HttpResponseRedirect('/ticwiapp/desktop', args)
    else:
	return render_to_response('invalid_login.html')

def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    else:
        form = MyRegistrationForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('register.html', args)

def register_success(request):
    return render_to_response('register_success.html',
			      {'full_name': request.user.username})

class ContactWizard(SessionWizardView):
    template_name = "contact_form.html"

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list)
        return render_to_response('done.html', {'form_data': form_data})


def process_form_data(form_list):
    form_data = [form.cleaned_data for form in form_list]

    logr.debug(form_data[0]['subject'])
    logr.debug(form_data[1]['sender'])
    logr.debug(form_data[2]['message'])

    send_mail(form_data[0]['subject'],
              form_data[2]['message'], form_data[1]['sender'],
              ['kozlex@hotmail.com'], fail_silently=False)

    return form_data


                             
