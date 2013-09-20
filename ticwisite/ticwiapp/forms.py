from django import forms
from models import Course,TicCategory,Tic, CourseComment, InboxMessage
from django.contrib.admin import widgets                                       
from django.forms.extras.widgets import SelectDateWidget

class CourseForm(forms.ModelForm):
    date  = forms.DateField(widget=SelectDateWidget() )

    class Meta:
        model = Course
	fields = ('name', 'date', 'description', 'importance')

class TicForm(forms.ModelForm):
    class Meta:
        model = Tic
        fields = ('dummy_name',)

class CourseCommentForm(forms.ModelForm):

    class Meta:
        model = CourseComment
        fields = ('first_name', 'second_name', 'body')

class InboxMessageForm(forms.ModelForm):

    class Meta:
        model = InboxMessage
        fields = ('body',)

