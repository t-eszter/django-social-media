from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from .models import Profile, Post, PostLikes, Followers
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

from .serializers import profileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@login_required(login_url='sign_in')

def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)

    all_users = Profile.objects.all().exclude(user=request.user)
    followed_profiles = Followers.objects.filter(following=user_object)

    #only show posts from followed users

    profile_ids = followed_profiles.values_list('follower__id', flat=True)
    feed = Post.objects.filter(user_id__in=profile_ids).order_by('-date')

    #suggesting users to follow

    suggested_profiles = Profile.objects.all().exclude(user=request.user).exclude(user__in=followed_profiles.values_list('follower', flat=True))

    #friends list
    friends = Profile.objects.all().exclude(user=request.user).filter(user__in=followed_profiles.values_list('follower', flat=True))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed, 'suggested_profiles': suggested_profiles, 'friends': friends})

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = PostLikes.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        # user has not liked the post yet
        new_like = PostLikes.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes = post.likes + 1
        post.save()
        return redirect('/')
    else:
        # user has already liked the post
        like_filter.delete()
        post.likes = post.likes - 1
        post.save()
        return redirect('/')

# R1 a) Users can create accounts
def sign_up(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('sign_up')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'User with this email already exists.')
                return redirect('sign_up')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #login after sign up
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                user_model = User.objects.get(username=username)
                user_profile = Profile.objects.create(user=user_model, userid=user_model.id)

                return redirect('settings')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('sign_up')

    else:
        return render(request, 'sign_up.html', {})

# R1 b) Users can log in and log out
def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('sign_in')
    else:
        return render(request, 'sign_in.html', {})


# R1 b, Users can log out
def log_out(request):
    auth.logout(request)
    return redirect('sign_in')

#R1 c) Users can search for other users
@login_required(login_url='sign_in')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    #search for user
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        searched_profile =[]
        searched_list =[]

        for users in username_object:
            searched_profile.append(users.id)

        for ids in searched_profile:
            profile_list = Profile.objects.filter(userid=ids)
            searched_list.append(profile_list)
        
        searched_list = list(chain(*searched_list))

        
    return render(request, "search.html", {'user_profile': user_profile, 'searched_list': searched_list, 'username': username})


# R1 d) Users can add other users as friends
@login_required(login_url='sign_in')
def followers(request):
    if request.method == 'POST':
        follower = request.POST['follower'] #user who is being followed: Testimo
        following = request.POST['following'] #user who is following: Teszter

        follower_object = User.objects.get(username = follower)
        following_object = User.objects.get(username = following)

        print(follower_object)
        print(following_object)

        followed = Followers.objects.filter(follower=follower_object, following=following_object).exists()

        if followed:
            Followers.objects.filter(follower=follower_object, following=following_object).delete()
        else:
            Followers.objects.create(following=following_object, follower=follower_object)

        return redirect('/profile/' + follower)
    
    else:
        return redirect('/')


# R1 e) Users can chat in realtime with friends
def chatIndex(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

# R1 f) Users can add status updates to their home page
@login_required(login_url='sign_in')
def post(request):
    return HttpResponse('Post')

# R1 g) Users can add media (such as images to their account and these are 	accessible via their home page
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')

    else:
        return redirect('/')

# You should collect and store an appropriate amount of information about each user (e.g. user name, use picture).
@login_required(login_url='sign_in')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image', user_profile.profile_img)
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')

    return render(request, 'user_settings.html', {'user_profile': user_profile})


def profile(request, username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object).order_by('-date')
    number_of_posts = Post.objects.filter(user=user_object).count()

    following_object = User.objects.get(username = request.user.username)

    followed = Followers.objects.filter(follower=user_object, following=following_object).exists()
    follow_btn = 'Remove friend' if followed else 'Add friend'


    followers=len(Followers.objects.filter(follower=user_object))
    following=len(Followers.objects.filter(following=user_object))


    context = {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_object' : user_object,
        'number_of_posts': number_of_posts,
        'follow_btn': follow_btn,
        'followers': followers,
        'following': following
    }

    return render(request, 'user_profile.html', context)


# API views

class profileList(APIView):
    def get(self, request):
        profile = Profile.objects.all()
        serializer = profileSerializer(profile, many=True)
        return Response(serializer.data)

    def post(self):
        pass
