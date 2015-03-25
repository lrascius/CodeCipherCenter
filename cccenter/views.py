import json
from django.shortcuts import render
from django.http import HttpResponse
import python.general as general
import python.cipher as cf
from random import randint

def index(request):
    #return HttpResponse("Hello, World!") # should really return the homepage
    return render(request, 'cccenter/cnc.html')
    
def getCipher(request):
    cipher = {}
    text = general.generate_paragraph()
    cipher['text'] = text
    cipher['cipher'] = cf.ceasar_shift_encode(text, randint(2,9))
    return HttpResponse(json.dumps(cipher['cipher']), content_type = "application/json")
