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

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(username=email, password=password)
                if(user):
                    return render(request, "dashboard.html", {'form': form})
                else:
                    messages.error(request, "Email or password not matching")
                    return render(request, "login.html", {'form': form})
            except Exception as e:
                messages.error(request, e)
                return render(request, "login.html", {'form': form})
    form = LoginForm()
    return render(request,"login.html", {'form':form})

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
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            # username=email, email=username this is for purpose. so user will login by its email
            try:
                user = User.objects.create_user(username=email, email=username, password=password)
                user.save()
            except Exception as e:
                messages.error(request, e)
                return render(request, "register.html", {'form': form})
            return redirect('/interface/login')
        return render(request, "register.html", {'form': form})
    form = registerForm()
    return render(request,"register.html", {'form': form})


