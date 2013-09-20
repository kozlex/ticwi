from django.contrib import admin
from ticwiapp.models import Course,TicCategory, WhoPresent, WhoParticipate
from profilemanager.models import CustomUser

#Here we are adding those tables that will be managed at website.com/admin
admin.site.register(Course)
admin.site.register(TicCategory)
admin.site.register(WhoPresent)
admin.site.register(WhoParticipate)
admin.site.register(CustomUser)
