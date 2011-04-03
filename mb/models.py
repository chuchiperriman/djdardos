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

class FollowingManager(models.Manager):
    
    def is_following(self, follower, followed):
        try:
            following = self.get(follower_object_id=follower.id, followed_object_id=followed.id)
            return True
        except Following.DoesNotExist:
            return False
    
    def follow(self, follower, followed):
        if follower != followed and not self.is_following(follower, followed):
            Following(follower_content_object=follower, followed_content_object=followed).save()
    
    def unfollow(self, follower, followed):
        try:
            following = self.get(follower_object_id=follower.id, followed_object_id=followed.id)
            following.delete()
        except Following.DoesNotExist:
            pass


class Following(models.Model):
    follower_content_type = models.ForeignKey(ContentType, related_name="followed")
    follower_object_id = models.PositiveIntegerField()
    follower_content_object = generic.GenericForeignKey('follower_content_type', 'follower_object_id')
    
    followed_content_type = models.ForeignKey(ContentType, related_name="followers")
    followed_object_id = models.PositiveIntegerField()
    followed_content_object = generic.GenericForeignKey('followed_content_type', 'followed_object_id')
    
    objects = FollowingManager()
