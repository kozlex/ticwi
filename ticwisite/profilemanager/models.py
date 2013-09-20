from django.db import models
from django.contrib.auth.models import User, UserManager
from ticwiapp.models import Inbox
class CustomUser(User):
    """User with app settings."""
    USER_TYPE = (
    ("i", 'Institution'),
    ("u", 'Participant AND Presenter'),
    )
    user_type       =       models.CharField( max_length=1 , default="i", choices=USER_TYPE)

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

