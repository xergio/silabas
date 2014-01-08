# -*- coding: utf-8 -*- 

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django import forms
from django.core.mail import send_mail
import home.silabea
import re
import redis


class ContactForm(forms.Form):
    message = forms.CharField()
    sender = forms.EmailField()


class SilabasForm(forms.Form):
    texto = forms.CharField()
    union = forms.BooleanField(required=False)
    
    
def index(request):
    response = {}
    r = redis.StrictRedis(host='localhost')
    
    
    if 'texto' in request.GET:
        sform = SilabasForm(request.GET)
 
        if sform.is_valid():
            k = "silabas:tmp:"+sform.cleaned_data['texto'].strip()
            antiflood = r.get(k)
            if antiflood is not None and int(antiflood) > 2:
                return render_to_response('home/flood.html', response)
            r.incr(k)
            r.expire(k, 3)
            
            response['lista_silabas'] = []
            texto = re.sub(u"[^a-zA-ZñÑáéíóúüÁÉÍÓÚÜ ]", "", sform.cleaned_data['texto'])
            
            if sform.cleaned_data['union']:
                texto = texto.replace(" ", "")
                
            for palabra in texto.split(" "):
                if palabra.strip() != '':
                    response['lista_silabas'].append( {'palabra': palabra, 'silabas': home.silabea.silabas(palabra.strip())} )
                
                    p = home.silabea.minusculas(palabra)
                    if not sform.cleaned_data['union']:
                        r.lpush("silabas:recent", p)
                        r.ltrim("silabas:recent", 0, 99)
                        r.zincrby("silabas:mostused", p, 1)
                        r.sadd("silabas:all", p)
                    r.incr("silabas:counter")
                
    else:
        sform = SilabasForm(initial={'texto': ''})
    
        
    if request.method == 'POST':
        cform = ContactForm(request.POST)
        if cform.is_valid():
            send_mail("Info sílabas", cform.cleaned_data['message'], cform.cleaned_data['sender'], ['xergio@gmail.com'])
    else:
        cform = ContactForm(initial={'message': '', 'sender': ''})
    
        
    response['sform'] = sform
    response['cform'] = cform
    
    response['randoms'] = set()
    silabas_all_len = r.scard("silabas:all")
    while len(response['randoms']) < 15 and silabas_all_len > len(response['randoms']):
        response['randoms'].add( r.srandmember("silabas:all") )
    
    response['mostused'] = r.zrevrange("silabas:mostused", 0, 14)
    
    if 'lista_silabas' in response and len(response['lista_silabas']) == 1:
        response['title'] = response['lista_silabas'][0]
    
    response.update(csrf(request))
    
    return render_to_response('home/index.html', response)
