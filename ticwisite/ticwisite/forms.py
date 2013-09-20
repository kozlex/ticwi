from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from profilemanager.models import CustomUser
import hashlib

class MyRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
	fields = ('email',  'user_type', 'password1', 'password2')
	#authenticate by email only
	unique_together = ('email',)
    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
 	#username should be filled and unique, lets add sha data
	#user.username = hashlib.sha256(user.email).hexdigest()[:30]
        # Or use email as unique:
        user.username = user.email

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)
	#Follow add some style to the input fields
	#TODO: Migrate formsty to a template?
        self.fields['email'].widget.attrs.update({'class' : 'formstyle'})
	self.fields['user_type'].widget.attrs.update({'class' : 'formstyle'})
	self.fields['password1'].widget.attrs.update({'class' : 'formstyle'})
	self.fields['password2'].widget.attrs.update({'class' : 'formstyle'})
	# Follow line 'removes' from the form tha username input field when rendered to html
	self.fields.pop('username')

class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)

class ContactForm2(forms.Form):
    sender = forms.EmailField()

class ContactForm3(forms.Form):
    message = forms.CharField(widget=forms.Textarea)




