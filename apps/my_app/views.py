# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Poke
from django.db.models import Count, Sum

# Create your views here.

def index(request):
    if 'id' in request.session:
        return redirect('/pokes')
    return render(request, "my_app/index.html")


def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    c_password = request.POST['c_password']
    birthday = request.POST['birthday']
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Validation errors
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')

    # Create new user
    User.objects.create(name=name, alias=alias, email=email, birthday=birthday, password=hashed_pw)

    messages.success(request, "Successfully registered!")
    return redirect('/')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    # Check user's password
    user = User.objects.filter(email=email)
    if len(user) > 0:
        checkPassword = bcrypt.checkpw(password.encode(), user[0].password.encode())
        if checkPassword:
            request.session['id'] = user[0].id
            return redirect('/pokes')

        else:
            messages.error(request, "Incorrect username or password")
            return redirect('/')
    else:
		messages.error(request, "Username and password fields are required")
		return redirect('/')


def pokes(request):
    logged_user = User.objects.get(id=request.session['id'])
    other_users = User.objects.exclude(id=request.session['id'])
    poker_name = Poke.objects.filter(poked=logged_user)
    user_poked = Poke.objects.filter(poked=logged_user)
    total_poked_by = Poke.objects.filter(poked=request.session['id']).count()
    total_pokes = User.objects.exclude(id=request.session['id']).annotate(counter=Sum("pokereceiver__num_pokes"))

    context = {
        "user": logged_user,
        "other_users": other_users,
        "poker_name": poker_name,
        "total_poked_by": total_poked_by,
        "user_poked": user_poked,
        "total_pokes":total_pokes
    }
    return render(request, "my_app/poke.html", context)


def poke_action(request, user_id):
    poker = User.objects.get(id=request.session['id'])
    poked = User.objects.get(id=user_id)
    pokes = Poke.objects.filter(poker=poker, poked=poked)

    if not pokes:
        Poke.objects.create(poker=poker, poked=poked, num_pokes=1)
        return redirect('/pokes')
    else:
        pokes[0].num_pokes += 1
        pokes[0].save()
        return redirect('/pokes')


def logout(request):
    request.session.clear()
    return redirect('/')