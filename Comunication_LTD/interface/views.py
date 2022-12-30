
from django.shortcuts import render, redirect
from .forms import *
#from termcolor import colored
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from interface.models import CustomUser, Customer,CustomUserPasswordHistory
from django.conf import settings
from config import db_name
import config
from django.contrib.auth import signals

from django.db import connection
import datetime

#TODO: implement go-back browser button redirect to login, to dashboard, registernewcustomers, customers
def is_logged_in(request):
    if config.sec_lvl == 'high' and not request.user.is_authenticated:
        return False
    elif config.sec_lvl == 'low' and request.session['user'] == '':
        return False
    return True

def dashboard(request):
    if not is_logged_in(request):
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
        if config.sec_lvl == 'high':
            user = authenticate(request, username=username, password=password)
            print(type(user))
            if user is None:
                messages.error(request, "Password or username is incorrect")
                return redirect('/interface/login')

            else: # username and password is correct
                login(request, user)
                return redirect('/interface/dashboard')

        elif config.sec_lvl == 'low':
            sqlQuery = "SELECT 1 FROM interface_customuser WHERE username = '%s' AND password = '%s'" % (username, password)
            isValidUser = False
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery)
                isValidUser = len(cursor.fetchall()) > 0

            # In case the password is not matching to the correct one
            if not isValidUser:
                # inform django-axes of failed login
                signals.user_login_failed.send(
                    sender=CustomUser,
                    request=request,
                    credentials={
                        'username': username,
                    },
                )
                messages.error(request, "Password or username is incorrect")
                return redirect('/interface/login')

            else:  # username and password is correct
                sqlQuery=f"DELETE FROM {db_name}.axes_accessattempt WHERE username = '{username}'"
                with connection.cursor() as cursor:
                    cursor.execute(sqlQuery)
                request.session['user'] = username
                return redirect('/interface/dashboard')

    else: # [GET] loading login form
        if 'security_btn' in request.GET:
            config.sec_lvl = 'low' if config.sec_lvl == 'high' else 'high'
        form = LoginForm()
        return render(request,"login.html", {'form':form,'sec_lvl':config.sec_lvl })

def logoutView(request):
    if is_logged_in(request):
        if config.sec_lvl == 'high':
            logout(request)
        elif config.sec_lvl == 'low':
            request.session['user'] = ''
    return redirect('/interface/login')

def register(request):
    print(config.sec_lvl)
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
            return redirect('/interface/register')

        if CustomUser.objects.filter(email = email).exists():
            messages.error(request, "Email already registered")
            return redirect('/interface/register')

        if config.sec_lvl == 'high':
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
        elif config.sec_lvl == 'low':
            sqlQuery = f"INSERT INTO interface_customuser (is_superuser, first_name, last_name, is_staff, is_active, date_joined, username, email, password) VALUES (0, '', '', 0, 1, %s, '{username}', '{email}', '{password}')"
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery, [datetime.datetime.now()])
            CustomUserPasswordHistory.remember_password(CustomUser.objects.get(username=username))
        messages.success(request, "Your account has been created.")
        return redirect('/interface/login')

    else: # [GET] loading register form
        form = CustomUserCreationForm()
        return render(request,"register.html", {'form': form})

def registerCustomer(request):
    if not is_logged_in(request):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    form = registerCustomerForm()

    if request.method == "POST": # user is trying to signup
        form = registerCustomerForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html", {'form': form})
        firstName = form.cleaned_data['firstName']
        lastName = form.cleaned_data['lastName']
        username = request.user if config.sec_lvl == 'high' else request.session['user']

        if config.sec_lvl == 'high':
            customer = Customer.objects.create(customerFirstName=firstName, customerLastName=lastName,username=username)
            customer.save()
        elif config.sec_lvl == 'low':
            sqlQuery = "INSERT INTO project_hit.interface_customer (username, customerFirstName, customerLastName) VALUES ('%s', '%s', '%s')" % (username, firstName, lastName)
            with connection.cursor() as cursor:
                cursor.execute(sqlQuery)

        messages.success(request, "Your account has been created.")
        return redirect('/interface/customers')
    else:
        return render(request, "registerCustomer.html", {'form': form})


def customers(request):
    if not is_logged_in(request):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    userId = request.user if config.sec_lvl == 'high' else request.session['user']
    customers = Customer.objects.filter(username=userId)
    firstNames = list(customers.values_list('customerFirstName',flat=True))
    lastNames = list(customers.values_list('customerLastName',flat=True))

    res = dict(map(lambda i, j: (i, j), firstNames, lastNames))

    return render(request, "customers.html",{'res':res})

def lockout(request, credentials, *args, **kwargs):
    messages.warning(request, "User has been locked out!")
    return render(request, "login.html", {'form': LoginForm()})


