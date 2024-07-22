from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_user_permissions'


AbstractUser._meta.get_field('groups').remote_field.related_name = 'auth_user_groups'
AbstractUser._meta.get_field('user_permissions').remote_field.related_name = 'auth_user_user_permissions'