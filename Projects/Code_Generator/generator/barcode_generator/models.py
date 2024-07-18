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

class Barcode(models.Model):
    barcode_number = models.CharField(max_length=13)
    image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    folder_name = models.CharField(max_length=100, default='default_folder_name')

    def __str__(self):
        return self.barcode_number
    
