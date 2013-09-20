from django import forms
from models import UserProfile, InstProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile 
        fields = ('second_name', 'birthday', 'gender')

class InstProfileForm(forms.ModelForm):
    class Meta:
        model = InstProfile
        fields = ('address', 'city', 'country','category')

