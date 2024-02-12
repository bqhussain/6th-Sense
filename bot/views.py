from django.shortcuts import render, redirect, render_to_response
import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings

# Create your views here.

class ChatterBotAppView(TemplateView):
    template_name = 'bot/app.html'


class ChatterBotApiView(View):


    chatterbot = ChatBot(**settings.CHATTERBOT,
                         filters=["chatterbot.filters.RepetitiveResponseFilter"])

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)


        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })