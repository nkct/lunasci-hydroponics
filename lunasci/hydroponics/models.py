from django.db import models

# Create your models here.

class Hydroponics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='hydroponics', on_delete=models.CASCADE)
    