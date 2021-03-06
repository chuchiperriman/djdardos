# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-
from djdardos.mb.models import *
from djdardos.dardos.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.generic.list_detail import object_list

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        exclude = ['sender_type', 'sender_id', 'sent']

def list(request, extra = None):
    return direct_to_template (request, template='mb/list.html',
                   extra_context=extra)

def new_tweet(request):
    if request.method == 'POST':

        form = TweetForm(data=request.POST)

        if form.is_valid():
            new_tweet = form.save(commit=False)
            tipo, id = request.POST["origen"].split('_')
            if tipo == 'jugador':
                new_tweet.sender = Jugador.objects.get(pk=id)
            elif tipo == 'equipo':
                new_tweet.sender = Equipo.objects.get(pk=id)
            else:
                raise Exception("Operación no permitida")
            new_tweet.save()
            return HttpResponseRedirect('/mb/list')
            #return HttpResponseRedirect(new_snippet.get_absolute_url())
    else:
        form = TweetForm()

    return list(request, {'form': form})

new_tweet = login_required(new_tweet)

def follow (request, content_type_id, object_id):
    ct = ContentType.objects.get(pk=content_type_id)
    #obj = ct.model_class().objects.get(pk=object_id)
    obj = get_object_or_404 (ct.model_class(), pk=object_id)
    print "..",ct, dir(ct), obj
    Following.objects.follow(request.user, obj)

    
    
