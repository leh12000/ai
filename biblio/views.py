import re

import openai
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book,Chapter
from  category.models import Category
from django.core.paginator import Paginator

from google.cloud import texttospeech

from ai import settings
from openai import OpenAI
import os
import google.generativeai as genai
from requests.auth import HTTPBasicAuth
import spacy

# Charger le modèle anglais
nlp = spacy.load('en_core_web_sm')



apikey = 'qbtj6epkpOVZ3mgJ98mQmxpCJWbCwCME0h2d-ouI7BYE'
url = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/edf80d88-61a8-41c7-896c-21f2f3f767ea/v1/synthesize'



headers = {
    'Content-Type': 'application/json',
    'Accept': 'audio/wav'
}


def format_response_with_spacy(text):
    doc = nlp(text)
    formatted_text = ""

    for sent in doc.sents:  # Parcours des phrases détectées par spaCy
        sent_text = sent.text.strip()

        if sent_text.startswith('-'):
            if not formatted_text.endswith('<ul>'):
                formatted_text += '<ul>'
            formatted_text += f'<li>{sent_text[1:].strip()}</li>'
        else:
            if formatted_text.endswith('</li>'):
                formatted_text += '</ul>'
            formatted_text += f'<p>{sent_text}</p>'

    if formatted_text.endswith('</li>'):
        formatted_text += '</ul>'

    return formatted_text


def format_response(text):
    # Supposons que l'API renvoie des éléments séparés par des sauts de ligne
    lines = text.split('\n')
    formatted_text = ""

    for line in lines:
        line = line.strip()
        if line.startswith('- '):  # Suppose que les listes commencent par "- "
            if not formatted_text.endswith('<ul>'):
                formatted_text += '<ul>'
            formatted_text += f'<li>{line[2:]}</li>'
        else:
            if formatted_text.endswith('</li>'):
                formatted_text += '</ul>'
            formatted_text += f'<p>{line}</p>'

    if formatted_text.endswith('</li>'):
        formatted_text += '</ul>'

    return formatted_text


def enlever(chaine):
    return re.sub(r'[^A-Za-z0-9]','',chaine)

# Create your views here.
def biblio(request):
    books=Book.objects.all()
    categories=Category.objects.all()
    print(categories)
    print("ok")
    return render(request,"sewa/mylearning.html",{"books":books,"categories":categories})


def details(request,book_id):

    book=Book.objects.get(id=book_id)
    chapters=Chapter.objects.filter(book=book)
    chapters=chapters.all()



    return render(request,"biblio/details.html",{"book":book})

genai.configure(api_key="AIzaSyCJ-eVPSyXTeKmCcWnnL-PT2xD8QdRwN7I")
generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
    history=[

    ]
)
def askAI(message):




    # Create the model


    response = chat_session.send_message(message)

    return response.text


def chatbox(request):
    if request.method=="POST":
        message=request.POST.get("message")
        response=askAI(message)
        text = response
        audio_filename = f'audio_{enlever(message)}.wav'
        audio_file_path = os.path.join(settings.MEDIA_ROOT,"audio", audio_filename)
        data = {
            'text': text,
            'voice': 'en-US_LisaV3Voice',  # Choisissez la voix que vous souhaitez
            'accept': 'audio/wav'
        }
        answer = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth('apikey', apikey))
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(answer.content)
        print("Synthèse vocale terminée et sauvegardée dans 'output.wav'")


        print(response)

        return JsonResponse({"message":message,"response":format_response(response),'audio_url': f'/media/audio/{audio_filename}'})


    return render(request,"biblio/chatbox.html")


def contentBook(request,id_book):
    book=Book.objects.get(id=id_book)
    chapters=Chapter.objects.filter(book=book)
    paginator=Paginator(chapters,1)
    page_number = request.GET.get('page')
    chapter = paginator.get_page(page_number)
    return render(request, 'biblio/contentBook.html', {'chapter': chapter})

def learningmode(request):

    return render(request,"biblio/learningmode.html")

def pods(request):
    return render(request, "biblio/pods.html")