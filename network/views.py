from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.forms import ModelForm
from django.contrib import messages
from datetime import date, datetime
from django.core.paginator import Paginator


from .models import * 


class PostForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


@csrf_protect
def index(request, *kwargs):

    auth_user = request.user

    post_comment = PostForm()
    posts = Post.objects.all().order_by('-post_id')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    likes = Like.objects.all()

    if request.method == "POST":

        comment = PostForm(request.POST)
        post = Post()

        #Get time
        post.post_date = datetime.now().replace(microsecond=0)

        #Get user name
        post.post_username = request.user
        post.post_user_id = request.user.id

        post.post_comments = comment.data['comment']
 
        post.save()

        messages.add_message(request, messages.SUCCESS, 'Message posted!')

        return render(request, "network/index.html", {'auth_user': auth_user,'form': post_comment, 'page_obj': page_obj, 'likes': likes})

    if request.method == "GET":

        #count number of likes
        return render(request, "network/index.html", {'auth_user': auth_user, 'form': post_comment, 'page_obj': page_obj, 'likes': likes})




def all_posts(request, *kwargs):

    posts = Post.objects.all().order_by('-post_id')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    likes = Like.objects.all()

    auth_user = request.user

    return render(request, "network/posts.html", {'auth_user': auth_user, 'page_obj': page_obj, 'likes': likes})


def profile(request, user_id):

    auth_user = request.user
    
    #Get this profile followers
    user = User.objects.get(pk=user_id)
    followers = Follow.objects.all().filter(user_id=user_id)
    totalFollowers = followers.count() 
    

    #Count this profile followings
    followings = Follow.objects.all().filter(following_id=user_id)
    totalFollowing = followings.count()
    

    #Get this profile posts
    username = user.username
    posts = Post.objects.all().order_by('-post_id').filter(post_username=username)

    
    #verify is auth_user is already following this profile
    is_following = Follow.objects.all().filter(user_id=request.user.id).filter(following_id=user_id)
    print(is_following)
    
    if not is_following :
        is_following = False
    else:
        is_following = True 

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    likes = Like.objects.all()

    return render(request, "network/profile.html", {'user': user, 'auth_user': auth_user, 'totalFollowing': totalFollowing, 'totalFollowers': totalFollowers, 'is_following': is_following, 'page_obj': page_obj, 'likes': likes})



def follow(request, user_id):

    follow = Follow()

    #Get user name
    follow.user_id = request.user.id
    follow.following_id = user_id

    follow.save()

    messages.add_message(request, messages.SUCCESS, 'You are now following this user')
    return redirect('profile', user_id=user_id)


#Get all posts form auth_user followings
def following(request):

    auth_user = request.user

    #Followers should be an array of user_id
    followings = Follow.objects.all().filter(user_id=auth_user.id)

    if not followings:

        messages.add_message(request, messages.SUCCESS, 'You are not following any profiles. Sorry! No post to show.')
        return render(request, "network/posts.html", {'posts': "", 'auth_user': auth_user}, )

    else:

        following_ids = [] 
        #Create a list of following ids
        for following in followings:
            following_ids.append(following.following_id)

        following_posts = Post.objects.all().order_by('-post_id').filter(post_user_id__in=following_ids)

        paginator = Paginator(following_posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        return render(request, "network/posts.html", {'page_obj': page_obj, 'auth_user': auth_user})



#Save the edit of a tweet  #*kwargs
def edit_tweet(request):

    new_text = request.GET.get('new_text', None)
    tweet_id = request.GET.get('tweet_id', None)
    
    the_post = Post()

    Post.objects.filter(pk=tweet_id).update(post_comments=new_text)

    data = { 'saved': "Tweet updated"}
    
    return JsonResponse(data)



#Save the edit of a tweet  #*kwargs
def like_tweet(request):

    tweet_id = request.GET.get('tweet_id', None)

    the_like = Like()

    the_like.post_id = tweet_id
    the_like.username_id = request.user.id

    the_post = Post.objects.get(pk=tweet_id)
    likes_num = the_post.post_likes

    if likes_num:
        new_like = int(likes_num) + 1
    else:
        new_like = 1

    Post.objects.filter(post_id=tweet_id).update(post_likes=new_like)
    the_like.save()

    data = { 'saved': "Tweet liked"}

    return JsonResponse(data)


#Save the edit of a tweet  #*kwargs
def unlike_tweet(request):

    tweet_id = request.GET.get('tweet_id', None)

    username_id = request.user.id

    Like.objects.filter(post_id=tweet_id).filter(username_id=username_id).delete()

    the_post = Post.objects.get(pk=tweet_id)
    likes_num = the_post.post_likes

    if likes_num:
        new_like = int(likes_num) - 1
    else:
        new_like = 0

    Post.objects.filter(post_id=tweet_id).update(post_likes=new_like)

    data = { 'saved': "Tweet unliked"}
    
    return JsonResponse(data)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
