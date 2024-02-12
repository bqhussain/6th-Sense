from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Chat(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    reciever = models.TextField()
    message = models.TextField()

    def __str__(self):
        return 'MessageObject'

    def last_10_messages(self):
        return Chat.objects.order_by('-created').all()[:10]