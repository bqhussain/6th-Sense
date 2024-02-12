from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from website import settings
from django.contrib.auth.models import User
from django.db.models import Q
from therapist.models import Appointment
import json
from django.core import serializers
from datetime import datetime

from .models import Chat
from django.utils import timezone



def ChatWindow(request):
    # c = Chat.objects.all()
    timecurrent = datetime.now()
    print(timecurrent)

    user_list = []
    if (request.user.profile.is_therapist):
        get_user = Appointment.objects.filter(therapist_id=request.user.profile.therapist.id, approved=2,payed=True,appointmenttime__lte=timecurrent,valid_till__gte=timecurrent)

        for users in get_user:
            user_list.append(users.user)
    else:
        get_user = Appointment.objects.filter(user_id=request.user.id, approved=2,payed=True,appointmenttime__lte=timecurrent,valid_till__gte=timecurrent)
        for therapists in get_user:
            user_list.append(therapists.therapist.pdetails.user)

    # Select therapist_therapist.* from appointments WHERE appoitnment_time <= CURRENT_TIME AND appointment_active_till >=
    # CURRENT_TIME AND user_id = LOGGED_IN_USER JOIN therapist_therapist ON therapist_therapist.id = appointments.therapist_id
    # AND approved = 2 AND payed = 1

    return render(request, 'livechat/chat.html', {'all_users': user_list})


# def Home(request):
#     c = Chat.objects.all()
#     return render(request, "alpha/home.html", {'home': 'active', 'chat': c})

# def Post(request):
#     if request.method == "POST":
#         msg = request.POST.get('msgbox', None)
#         c = Chat(user=request.user, message=msg)
#         if msg != '':
#             c.save()
#         return JsonResponse({ 'msg': msg, 'user': c.user.username })
#     else:
#         return HttpResponse('Request must be POST.')

# def Messages(request):
#     c = Chat.objects.all()
#
#     get_user = User.objects.all()
#     return render(request, 'alpha/messages.html', {'chat': c , 'all_users': get_user})

def saveMessage(req):
    sender_user = req.POST.get('sender', 1)
    reciever_user = req.POST.get('reciever', 2)
    message = req.POST.get('msg', 'HEY')

    senderobj = User.objects.get(id=sender_user)
    # recieverobj = User.objects.filter(id=reciever_user)

    c = Chat(sender=senderobj, reciever=reciever_user, message=message)
    if message != '':
        c.save()
        return JsonResponse({'msg': message})
    else:
        return HttpResponse('Msg field required')


def getMessages(req):
    sender_user = req.GET.getlist('reciever_id')

    message_list = Chat.objects.filter(Q(sender_id=req.user.id, reciever=sender_user[0])
                                       | Q(reciever=req.user.id, sender_id=sender_user[0])).values().order_by('created')

    # message_list = Chat.objects.raw('SELECT * FROM alpha_chat WHERE (reciever = sender_user[0] AND sender_id = req.user.id) OR (reciever = req.user.id AND sender_id = sender_user[0])')

    messageslists = {'message_list': list(message_list)}

    return JsonResponse(messageslists)
