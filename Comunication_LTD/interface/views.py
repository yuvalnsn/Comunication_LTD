from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect
from .forms import *
from termcolor import colored
from os import linesep as ln
from django.contrib import messages
# from interface.models import User
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def dashboard(request):

    return render(request,"dashboard.html", {})

# DOTO: fix login function, swap between username, and email in db
# In addition make code more readable
def login(request):
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
            return redirect('/interface/dashboard')

    else: # [GET] loading login form
        return render(request,"login.html", {'form': LoginForm()})
def logout(request):
    try:
        request.session.flush()
    except:
        print("Error")
        pass
    return redirect('/interface/login')


def forGotPassword(request):
    return render(request,"forGotPassword.html", {})


def register(request):
    if request.method == "POST": # user is trying to signup
        form = registerForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html", {'form': form})
    #     form is valid (password satisfies the conditions)
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        if User.objects.filter(username = username).exists():
            messages.error(request, "Username is already exists")
            return redirect('/interface/login')

        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already registered")
            return redirect('/interface/login')

    #     username and email are unique
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
    #     insert user into the db
        messages.success(request, "Your account has been created.")
        return redirect('/interface/login')

    else: # [GET] loading register form
        form = registerForm()
        return render(request,"register.html", {'form': form})