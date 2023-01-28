from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import ProfileDB

# Create your views here.



def Index(req):
    return render(req, 'index.html')


def Signin(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(req, user)
            return redirect('/')
        else:
            messages.info(req, 'Invalid login details')
            return redirect('Signin')
    else:
        return render(req, 'login1.html')


def Signup(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        password2 = req.POST.get('password2')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(req, 'Email already taken')
                return redirect('Signup')
            elif User.objects.filter(username=username).exists():
                messages.info(req, 'Username already taken')
                return redirect('Signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # after signing up redirecting the user to profile settings
                # Creating a profile object for the newly created user
                user_model = User.objects.get(username=username)
                new_profile = ProfileDB.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('Signup')
        else:
            messages.info(req, f'Password does not match')
            return redirect('Signup')
        
    else:
        return render(req, 'login.html')
