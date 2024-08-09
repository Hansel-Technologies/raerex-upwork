# admin_panel/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Superadmin'),
        (2, 'Admin'),
        (3, 'Editor'),
        (4, 'Viewer'),
    )
    
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)

    def is_superadmin(self):
        return self.user_type == 1

    def is_admin(self):
        return self.user_type == 2

    def is_editor(self):
        return self.user_type == 3

    def is_viewer(self):
        return self.user_type == 4