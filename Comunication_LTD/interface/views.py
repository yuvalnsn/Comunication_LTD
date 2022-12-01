from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect
from .forms import *
from termcolor import colored
from os import linesep as ln
from django.contrib import messages
# from interface.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from interface.models import CustomUser

from django.conf import settings


def dashboard(request):
    userId=request.user
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,"dashboard.html", {})

def login2(request):
    if request.method == "POST": # user is trying to signin
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request,"login.html", {'form': LoginForm()})
        #   form is valid
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Password or username is incorrect")
            return redirect('/interface/login')

        else: # username and password is correct
            login(request, user)
            return redirect('/interface/dashboard')

    else: # [GET] loading login form
        return render(request,"login.html", {'form': LoginForm()})

def logout(request):
    try:
        logout(request)
        request.session.flush()
    except:
        print("Error")
        pass
    return redirect('/interface/login')

def register(request):
    if request.method == "POST": # user is trying to signup
        form = CustomUserCreationForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html", {'form': form})
    #     form is valid (password satisfies the conditions)
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        if CustomUser.objects.filter(username = username).exists():
            messages.error(request, "Username is already exists")
            return redirect('/interface/login')

        if CustomUser.objects.filter(email = email).exists():
            messages.error(request, "Email already registered")
            return redirect('/interface/login')

    #     username and email are unique
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
    #     insert user into the db
        messages.success(request, "Your account has been created.")
        return redirect('/interface/login')

    else: # [GET] loading register form
        form = CustomUserCreationForm()
        return render(request,"register.html", {'form': form})