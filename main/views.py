from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

from .models import ProfileDB, PostDB, LikepostDB, FollowerDB

# Create your views here.


@login_required(login_url='Signin')
def Index(req):
    user_object = User.objects.get(username=req.user.username)
    user_profile = ProfileDB.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowerDB.objects.filter(follower=req.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_list = PostDB.objects.filter(user=usernames)
        feed.append(feed_list)

    feed_list = list(chain(*feed))
    random.shuffle(feed_list)

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=req.user.username)
    final_suggestions = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = ProfileDB.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(req, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions': suggestions_username_profile_list[:4]})


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

        return redirect('/')
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

@login_required(login_url='Signin')
def like_post(req):
    username = req.user.username
    post_id = req.GET.get('post_id')

    post = PostDB.objects.get(id=post_id)

    like_filter = LikepostDB.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikepostDB.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/') 

@login_required(login_url='Signin')
def Profile(req, pk):
    user_object = User.objects.get(username=pk)
    profile_object = ProfileDB.objects.get(user=user_object)
    post_object = PostDB.objects.filter(user=pk)
    user_post_length = len(post_object)

    follower = req.user.username
    user = pk

    if FollowerDB.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowerDB.objects.filter(user=pk))
    user_following = len(FollowerDB.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'profile': profile_object,
        'post': post_object,
        'no_of_posts': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }

    return render(req, 'profile.html', context)

@login_required(login_url='Signin')
def Follow(req):
    if req.method == 'POST':
        follower = req.POST.get('follow')
        user = req.POST.get('user')

        if FollowerDB.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowerDB.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('profile/'+user)
        else:
            new_follower = FollowerDB.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='Signin')
def Search(req):
    user_object = User.objects.get(username = req.user.username)
    user_profile = ProfileDB.objects.get(user=user_object)

    if req.method == 'POST':
        username = req.POST.get('username')
        username_object = User.objects.filter(username__contains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = ProfileDB.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))

    return render(req, 'search.html', {'user_profile': user_profile, 'user_profile_list': username_profile_list})
