from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateField, TextField, Model, OneToOneField, CASCADE


# Create your models here.
class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    birth_date = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)