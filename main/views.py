from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import ProfileDB,PostDB

# Create your views here.


@login_required(login_url='Signin')
def Index(req):
    user_object = User.objects.get(username=req.user.username)
    user_profile = ProfileDB.objects.get(user=user_object)

    post_feed = PostDB.objects.all()
    return render(req, 'index.html', {'user_profile': user_profile, 'posts': post_feed})


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

                # after signing up redirecting the user to profile settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(req, user_login)

                # Creating a profile object for the newly created user
                user_model = User.objects.get(username=username)
                new_profile = ProfileDB.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('Settings')
        else:
            messages.info(req, f'Password does not match')
            return redirect('Signup')
        
    else:
        return render(req, 'login.html')


@login_required(login_url='Signin')
def Logout(req):
    auth.logout(req)
    return redirect('Signin')

@login_required(login_url='Signin')
def Settings(req):
    user_profile = ProfileDB.objects.get(user=req.user)

    if req.method == 'POST':
        if req.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = req.POST.get('bio')
            location = req.POST.get('location')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if req.FILES.get('image') != None:
            image = req.FILES['image']
            bio = req.POST.get('bio')
            location = req.POST.get('location')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('Settings')
    return render(req, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='Signin')
def Upload(req):
    if req.method == 'POST':
        user = req.user.username
        image = req.FILES['image']
        caption = req.POST.get('caption')

        new_post = PostDB.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

