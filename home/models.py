from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_countries.fields import CountryField
import datetime
# from therapist.models import Therapist



# Create your models here.

class Profile(models.Model):
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=1, choices=GENDER, default='f')
    date_of_birth = models.DateField(default=datetime.date.today, max_length=8)
    address = models.TextField(default='clifton karachi')
    city = models.CharField(max_length=25,default='Karachi')
    country = CountryField(default='PK', blank_label='(select country)')
    is_therapist = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Questions(models.Model):

    question = models.TextField()

class Answers(models.Model):

    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    answer = models.CharField(max_length=1)

    def __str__(self):
        return f'{self.user.username} Answers'






