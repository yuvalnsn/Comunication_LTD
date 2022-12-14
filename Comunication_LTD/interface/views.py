
from django.shortcuts import render, redirect
from .forms import *
#from termcolor import colored
from django.contrib import messages
from django.contrib.auth import authenticate, login
from interface.models import CustomUser, Customer
from django.conf import settings
from config import sec_lvl

from django.db import connection
import datetime


def dashboard(request):
    userId=request.user
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,"dashboard.html", {})

def login2(request):
    if request.method == "POST": # user is trying to signin
        if sec_lvl == 'high':
            form = LoginForm(request.POST)
            if not form.is_valid():
                return render(request,"login.html", {'form': LoginForm()})
            #   form is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Password or username is incorrect")
                return redirect('/interface/login')

            else: # username and password is correct
                login(request, user)
                return redirect('/interface/dashboard')
        #TODO: fix implementation, pass username through the session (login(request, user))

        # elif sec_lvl == 'low':
        #     form = LoginForm(request.POST)
        #     if not form.is_valid():
        #         return render(request, "login.html", {'form': LoginForm()})
        #     #   form is valid
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        #
        #     # user = authenticate(request, username=username, password=password)
        #     sqlQuery = "SELECT 1 FROM WHERE username = '%s' AND password = '%s'"
        #     isValidUser = False
        #
        #     with connection.cursor() as cursor:
        #         cursor.execute(sqlQuery)
        #         isValidUser = len(cursor.fetchall()) > 0
        #
        #     # In case the password is not matching to the correct one
        #     if not isValidUser:
        #         messages.error(request, "Password or username is incorrect")
        #         return redirect('/interface/login')
        #
        #     else:  # username and password is correct
        #         login(request, user)
        #         return redirect('/interface/dashboard')

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
        if sec_lvl == 'high':
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
        elif sec_lvl == 'low':
            form = CustomUserCreationForm(request.POST)
            if not form.is_valid():
                return render(request, "register.html", {'form': form})
            #     form is valid (password satisfies the conditions)
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username is already exists")
                return redirect('/interface/login')

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect('/interface/login')

            sqlQuery = f"INSERT INTO interface_customuser (is_superuser, first_name, last_name, is_staff, is_active, date_joined, username, email, password) VALUES (0, '', '', 0, 0, %s, '{username}', '{email}', '{password}')"
            print(sqlQuery);

            with connection.cursor() as cursor:
                cursor.execute(sqlQuery, [datetime.datetime.now()])

            messages.success(request, "Your account has been created.")
            return redirect('/interface/login')

    else: # [GET] loading register form
        form = CustomUserCreationForm()
        return render(request,"register.html", {'form': form})

def registerCustomer(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = registerCustomerForm()

    if request.method == "POST": # user is trying to signup
        if sec_lvl == 'high':
            form = registerCustomerForm(request.POST)
            if not form.is_valid():
                return render(request, "register.html", {'form': form})
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            username = str(request.user)
            print(username)
            customer = Customer.objects.create(customerFirstName=firstName, customerLastName=lastName,username=username)
            customer.save()
            messages.success(request, "Your account has been created.")
            return redirect('/interface/customers')
        elif sec_lvl == 'low':
            form = registerCustomerForm(request.POST)
            if not form.is_valid():
                return render(request, "register.html", {'form': form})
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            username = str(request.user)

            sqlQuery = "INSERT INTO project_hit.interface_customer (username, customerFirstName, customerLastName) VALUES ('%s', '%s', '%s')" % (username, firstName, lastName)
            print(sqlQuery)

            with connection.cursor() as cursor:
                cursor.execute(sqlQuery)

            messages.success(request, "Your account has been created.")
            return redirect('/interface/customers')
    else:
        return render(request, "registerCustomer.html", {'form': form})


def customers(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    userId=request.user
    customers=Customer.objects.filter(username=userId)
    firstNames=list(customers.values_list('customerFirstName',flat=True))
    lastNames=list(customers.values_list('customerLastName',flat=True))
    res = dict(map(lambda i, j: (i, j), firstNames, lastNames))


    return render(request, "customers.html",{'res':res})
