
from django.db import models
from django.db.models import DateField, TextField, Model, OneToOneField, CASCADE, ForeignKey, DO_NOTHING, ImageField, \
    CharField
from django.contrib.auth.models import User

from viewer.models import Image


# Create your models here.


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    birth_date = DateField(null=True, blank=True, verbose_name='Datum narození')
    biography = TextField(null=True, blank=True, verbose_name='Biografie')


class UserImage(Model):
    user = ForeignKey(Profile, on_delete=DO_NOTHING)
    image = ImageField(upload_to='user_images/')
    description = CharField(max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            new_width = 300
            new_height = 200

            img = img.resite((new_width, new_height), Image.ANTIALIAS)

            img.save(self.image.path)

    def __str__(self):
        return self.description if self.description else "No description"
