# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User

# Create your models here.
class pokeManager(models.Manager):
    def add(self,for_user,from_user):
        print for_user.alias
        print from_user.alias
        try:
            pokes=self.get(for_user=for_user,from_user=from_user)
            pokes.poke +=1
            pokes.save()
        except:
            self.create(poke=1,for_user=for_user,from_user=from_user)

class Poke(models.Model):
    poke=models.IntegerField()
    for_user=models.ForeignKey(User,related_name="get_poke")
    from_user=models.ForeignKey(User,related_name="poked")
    created_at=models.DateTimeField(auto_now_add = True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=pokeManager()
