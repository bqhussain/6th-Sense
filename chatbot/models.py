from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BotChat(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    reciever = models.TextField()
    message = models.TextField()
    message_audio = models.FileField(default='empty',upload_to='bot_audio')

    def __str__(self):
        return 'BotMessageObject'

    def last_10_messages(self):
        return BotChat.objects.order_by('-created').all()[:10]


class WordBank(models.Model):
    word = models.CharField(max_length=255)
    score = models.IntegerField(default=0)


class WordMeter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    word = models.ForeignKey(WordBank,on_delete=models.CASCADE)
