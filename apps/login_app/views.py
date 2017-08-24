# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User

def sesssionCheck(request):
    try:
        return request.session['user_id']
    except:
        return False

# Create your views here.
def index(request):
    return render(request,"login_app/index.html")
def login(request):
    results=User.objects.loginValidator(request.POST)
    if results['status']==True:
        for error in results['errors']:
             messages.error(request,error)
        return redirect(index)
    else:
        request.session['id']=results['user'].id
        request.session['alias']=results['user'].alias
        return redirect("/pokes")

def registration(request):
    results=User.objects.registrationValidator(request.POST)
    if results['status']==True:
        for error in results['errors']:
             messages.error(request,error)
        return redirect(index)
    user=User.objects.creator(request.POST)
    messages.success(request,"User has been created. Please log in to continue.")
    return redirect(index)
