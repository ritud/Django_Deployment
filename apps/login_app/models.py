# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from time import gmtime, strftime
import datetime
from dateutil.parser import *
import re
import bcrypt
# Create your models here.
today = datetime.date.today()
bval = datetime.date(today.year - 18,today.month,today.day)
class UserManager(models.Manager):

    def loginValidator(self,postData):
        results={"status":False,"errors":[],"user":None}
        if not postData['email']:
            results['errors'].append("Email field can not be empty")
        else:
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w', postData['email']):
                results['errors'].append('Please enter a valid email')
            elif len(User.objects.filter(email=postData['email']))<1:
                results['errors'].append("You are not a Registered User ! Please Register !")
            else:
                if not postData['password']:
                    results['errors'].append("password field can not be empty")
                else:
                    user=self.get(email=postData['email'])
                    print user
                    if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                       results['errors'].append('Please enter valid password')
                    results['user']=user

        if len(results['errors'])>0:
            results['status']= True
        return results

    def registrationValidator(self,postData):
        results={"status":False,"errors":[]}
        if not postData['name']:
            results['errors'].append("Fisrt Name field can not be empty")
        else:
            if len(postData['name'])<3:
                results['errors'].append("Fist Name field can not have less than 3 characters")
        if not postData['alias']:
            results['errors'].append("Last Name field can not be empty")
        else:
            if len(postData['alias'])<3:
                results['errors'].append("Last Name field can not have less than 3 characters")
        if not postData['bday']:
            results['errors'].append("Birthday field can not be empty")
        else:
            if not re.match('(\d{4})[-](\d{2})[-](\d{2})$',postData['bday']):
                results['errors'].append("Please Enter Valid Birthday")
            else:
                now=strftime("%Y-%m-%d", gmtime())
                if postData['bday'] >now :
                    results['errors'].append("Your bday can not be in future")

            dd = postData['bday']
            try:
                db = datetime.date(int(dd[0:4]),int(dd[5:7]),int(dd[8:10]))
                if db > bval:
                    results['errors'].append("You are not 18 Years old")
            except:
                results['errors'].append("Please enter valid date of birth")

        if not postData['email']:
            results['errors'].append("Email field can not be emty")
        else:
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w', postData['email']):
                results['errors'].append('Please enter a valid email')
        if not postData['password']:
            results['errors'].append("password field can not be empty")
        else:
            if len(postData['password'])< 8:
                results['errors'].append('Your password must be more than 8 characters')
            else:
                if postData['password'] != postData['c_password']:
                    results['errors'].append('Your password must match')

        if len(self.filter(email=postData['email']))>0:
            results['errors'].append('User already exist')

        if len(results['errors'])>0:
            results['status']= True
        return results

    def creator(self,postData):
        hashed = bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt())
        user=User.objects.create(name=postData['name'],alias=postData['alias'],email=postData['email'],pokes=0,password=hashed,bday=postData['bday'])
        return user
    def addpoke(self,user_id):
        user=self.get(id=user_id)
        user.pokes +=1
        user.save()

class User(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    email=models.CharField(max_length=100)
    pokes=models.IntegerField()
    bday=models.DateField()
    password=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
