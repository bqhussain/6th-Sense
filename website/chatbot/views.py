import geocoder
from django.http import JsonResponse, HttpResponse
# from django.shortcuts import render


import dialogflow_v2 as dialogflow
# from eventbrite import Eventbrite
import requests
import json
from django.db.models import Q
from gtts import gTTS
import random
# # import pusher
# import urllib
# import os


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.models import User
from django.conf import settings
from .models import BotChat,WordBank as wb, WordMeter as wm


# @csrf_exempt
# @require_POST
# def webhook(request):
#     req = json.loads(request.body)
#     movie = req['queryResult']['parameters']['movie']
#
#     speech = 'Bekaar Movie Hai bhai mat dekhna'
#     # print("Request:")
#     # print(json.dumps(req, indent=2))
#     # res = makeWebhookResult(req)
#     # res = json.dumps(res, indent=2)
#     # reply = {
#     #     'speech': speech,
#     #     'displayTest': speech,
#     #     'source': 'ChatBot'
#     # }
#     reply = {
#         "fulfillmentText": speech,
#     }
#     # print(res)
#     # return res
#     # r = make_response(res)
#     # r.headers['Content-Type'] = 'application/json'
#     return JsonResponse(reply, status = 200)

def music_api(artistname):
    return 'song_request,{0}'.format(artistname)


def event_api(request,event_time):



    event_list = eventgetter(request,event_time)
    # print(event_list)
    if event_list is None:
        return 'No Events are there for that time'


    return 'event_requestæ{0}'.format(event_list)


def eventgetter(request,event_time):
    ip_address = request.META.get("REMOTE_ADDR")
    # event_time = request.GET.get('event_time')
    g = geocoder.ip(ip_address)
    # print(g.latlng)
    # print(g.lat)
    # print(g.lng)

    LATITUDE = 24.8270
    LONGITUDE = 67.0251
    START_DATE = event_time
    API_TOKEN = 'ZZQA7VNMYDDGHMU544S6'
    #
    event_search = requests.get(
        'https://www.eventbriteapi.com/v3/events/search/?location.within=10km&location.latitude={0}&location.longitude={1}&start_date.keyword={2}&token={3}'.format(
            LATITUDE, LONGITUDE, START_DATE, API_TOKEN)).content
    event_details = json.loads(event_search)

    event_list = json.dumps(event_details['events'])



    # for events in event_list:
    #     print(events['name']['text'], events['url'],events['logo']['original']['url'])

    eventsLists = {'eventsLists': event_list}

    # return JsonResponse(eventsLists)
    return event_list

    # eventbrite = Eventbrite('ZZQA7VNMYDDGHMU544S6')
    # data = {
    #     'location.latitude': '24.8270',
    #     'start_date.keyword': 'today',
    #     'location.longitude': '67.0251',
    #     'location.within': '10km'
    # }
    # events = eventbrite.event_search(**data)
    # print(type(events))
    # print(events.pretty)
    # import json
    # date = json.loads(events)
    #
    # print(date)
    # date = json.dumps(events)

    # return render(request, 'posts/location.html')


@csrf_exempt
@require_POST
def webhook(request):
    req = json.loads(request.body)

    action = req['queryResult']['action']

    if (action == 'getsong'):
        artist_name = req['queryResult']['parameters']['artists_name']
        song_list = music_api(artist_name)
        reply = {

            "fulfillmentText": song_list
        }
        return JsonResponse(reply, status=200)

    elif (action == 'event_search'):
        event_time = req['queryResult']['parameters']['events_around']
        events_list = event_api(request,event_time)
        reply = {

            "fulfillmentText": events_list
        }
        return JsonResponse(reply, status=200)

    speech = 'Bekaar Movie Hai bhai mat dekhna'
    # print("Request:")
    # print(json.dumps(req, indent=2))
    # res = makeWebhookResult(req)
    # res = json.dumps(res, indent=2)
    # reply = {
    #     'speech': speech,
    #     'displayTest': speech,
    #     'source': 'ChatBot'
    # }
    reply = {
        "fulfillmentText": speech,
    }
    # print(res)
    # return res
    # r = make_response(res)
    # r.headers['Content-Type'] = 'application/json'
    return JsonResponse(reply, status=200)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        a = type(response)
        import google.protobuf  as pf

        # messages = pf.json_format.MessageToJson(response.query_result.fulfillment_messages[1].text,
        #                              including_default_value_fields=False)
        messages = []

        for msg in response.query_result.fulfillment_messages:
            messages.append(msg.text.text[0])
        # messages.append(response.query_result.fulfillment_messages[0].text.text)
        # messages.append(response.query_result.fulfillment_messages[1].text.text)
        # messages.append(response.query_result.fulfillment_messages[2].text.text)
        # messages.append(response.query_result.fulfillment_messages[3].text.text)
        return messages
        # return response.query_result.fulfillment_text

def extracting_words(message,user_id):

    all_Words = wb.objects.all()
    new_message = str(message).lower()


    for words in all_Words:

        if words.word in new_message:
            wm.objects.create(user_id=user_id, word_id= words.id)

    return True


@csrf_exempt
@require_POST
def send_message(request):
    message = request.POST.get('msg', 'HEY')
    sender_user = request.POST.get('sender', 1)
    reciever_user = request.POST.get('reciever', 2)
    senderobj = User.objects.get(id=sender_user)
    recieverobj = User.objects.get(id=reciever_user)
    user_message = BotChat(sender=senderobj, reciever=reciever_user, message=message)
    if message != '':
        user_message.save()
        extracting_words(message, sender_user)
        # find word
    # message = request.POST['message']
    project_id = settings.DIALOGFLOW_PROJECT_ID
    fulfillment_text = detect_intent_texts(project_id, request.user.id, message, 'en')



    for messages in fulfillment_text:

        try:
            if('song_request' in messages or 'event_requestæ' in messages):
                bot_message = BotChat(sender=recieverobj, reciever=sender_user, message=messages)
                if messages != '':
                    bot_message.save()
            else:
                mytext = messages

                # Language in which you want to convert
                language = 'en'

                # Passing the text and language to the engine,
                # here we have marked slow=False. Which tells
                # the module that the converted audio should
                # have a high speed
                myobj = gTTS(text=mytext, lang=language, slow=False)

                # Saving the converted audio in a mp3 file named
                # welcome
                audio_path = f'bot_audio/{random.randint(1,100000000)}.mp3'
                path = f'/Users/Bilal/PycharmProjects/website/media/{audio_path}'
                myobj.save(path)
                bot_message = BotChat(sender=recieverobj, reciever=sender_user, message=messages, message_audio=audio_path)
                if messages != '':
                    bot_message.save()
        except Exception:
            bot_message = BotChat(sender=recieverobj, reciever=sender_user, message=messages)
            if messages != '':
                bot_message.save()
        # finally:
        #     if audio_path is None:
        #         audio_path= 'empty'
        #     bot_message = BotChat(sender=recieverobj, reciever=sender_user, message=messages,message_audio=audio_path)
        #     if messages != '':
        #         bot_message.save()

    response_text = {"bot_message": fulfillment_text, "user_message": message}

    return JsonResponse(response_text, status=200)


def getMessages(req):
    sender_user = req.GET.getlist('reciever_id')

    message_list = BotChat.objects.filter(Q(sender_id=req.user.id, reciever=sender_user[0])
                                          | Q(reciever=req.user.id, sender_id=sender_user[0])).values().order_by(
        'created')

    # message_list = Chat.objects.raw('SELECT * FROM alpha_chat WHERE (reciever = sender_user[0] AND sender_id = req.user.id) OR (reciever = req.user.id AND sender_id = sender_user[0])')


    messageslists = {'message_list': list(message_list)}

    return JsonResponse(messageslists)

# def makeWebhookResult(req):
#
#     if req.get('result').get('action') != 'movie':
#         return {}
#     result = req.get('result')
#     parameters = result.get('parameters')
#     moviename = parameters.get('movie')
#     if moviename == 'Black Panther':
#         speech = 'Bekaar Movie Hai Panther'
#     if moviename == 'The Mummy':
#         speech = 'Bekaar Movie Hai Mummy'
#     return {
#         'speech': speech,
#         'displayTest': speech,
#         'source': 'ChatBot'
#     }
