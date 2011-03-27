# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.
class Tweet(models.Model):
    """
    a single tweet from a user
    """
    
    text = models.CharField('text', max_length=140)
    sender_type = models.ForeignKey(ContentType)
    sender_id = models.PositiveIntegerField()
    sender = generic.GenericForeignKey('sender_type', 'sender_id')
    sent = models.DateTimeField('sent', default=datetime.now)
    
    def __unicode__(self):
        return self.text
    
    def get_absolute_url(self):
        return ("single_tweet", [self.id])
    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        ordering = ('-sent',)
