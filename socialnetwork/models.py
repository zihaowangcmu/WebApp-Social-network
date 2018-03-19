# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    picture = models.FileField(upload_to='images', blank=True)
    following = models.ManyToManyField('Profile', related_name='followed_by')
    # content_type checks the uploaded file is legal or not
    content_type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user.username+','+self.bio+',end'

# Everytime the User class create a new instance, so does the Profile class.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#Everytime the User instance is saved, so does the Profile class
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Posts(models.Model):
    content       = models.CharField(max_length=300)
    created_by    = models.ForeignKey(User, related_name="post_creators")
    creation_time = models.DateTimeField()
    created_by_username = models.CharField(max_length=100)
    created_by_identity = models.CharField(max_length=300)

    def __unicode__(self):
        return 'Posts(id=' + str(self.content) + ')'

# Data model for a todo-list item
class Comments(models.Model):
    content       = models.CharField(max_length=300)
    created_by    = models.ForeignKey(User, related_name="comment_creators")
    creation_time = models.DateTimeField()
    post          = models.ForeignKey(Posts, related_name="comments")
    created_by_username = models.CharField(max_length=100)

    def __unicode__(self):
        return self.content