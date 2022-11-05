from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect


def dashboard(request):
    # dataBase = mysql.connector.connect(
    #     host='127.0.0.1',
    #     user='root',
    #     password="hithit123"
    # )
    #
    # # preparing a cursor object
    # cursorObject = dataBase.cursor()
    #
    # # creating database
    # cursorObject.execute("CREATE DATABASE PROJECT_HIT")
    return render(request,"dashboard.html", {})

def login(request):

    return render(request,"login.html", {})

def logout(request):
    try:
        request.session.flush()
    except:
        print("Error")
        pass
    return redirect('/interface/login')

