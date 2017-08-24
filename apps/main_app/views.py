# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from models import User,Poke
# Create your views here.
def sessCheck(request):
    try:
        return request.session['id']
    except:
        return False

def index(request):
    if sessCheck(request) == False:
        return redirect('/')

    users=User.objects.all()
    try:
        uid=request.session['id']
        obj=User.objects.get(id=uid)
        pokes=Poke.objects.filter(for_user=obj).order_by('-poke')
        count=pokes.count()
    except:
        count=0
        pokes=None
    context={"users":users,"count":count,"pokes":pokes}
    return render(request,"main_app/index.html",context)

def process(request,user_id):
    uid=request.session['id']
    from_user=User.objects.get(id=uid)
    for_user=User.objects.get(id=user_id)
    User.objects.addpoke(user_id)
    Poke.objects.add(for_user,from_user)
    return redirect(index)

def logout(request):
    request.session.clear()
    return redirect('/')
