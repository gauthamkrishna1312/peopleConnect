from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profiles, Post, LikePost, FollowersCount

# Create your views here.


#to call home page
@login_required(login_url='signin')
def index(request):

    posts = Post.objects.all()
    return render(request, 'index.html', {'posts':posts})

#search for people
@login_required(login_url='signin')
def search(request):
    usrname = request.POST.get('username')
    results = User.objects.filter(username__icontains = usrname)
    context = {'results': results}
    return render(request, 'search.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.filter(follower=follower, user=user)
            delete_follower.delete()
            return redirect("/account/"+user)
        else :
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/account/"+user)
    else :
        return redirect('/')
    
#for profile page
@login_required(login_url='signin')
def account(request,usnm):
    user_object = User.objects.get(username = usnm)
    user_profile = Profiles.objects.get(user = user_object)
    user_post = Post.objects.filter(user = usnm)
    user_post_lenght = len(user_post)

    follower = request.user.username
    user = usnm

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else :
        button_text = 'follow'

    user_followers = len(FollowersCount.objects.filter(user = usnm))
    user_following = len(FollowersCount.objects.filter(follower = usnm))

    #for mutual followers
    current_user = request.POST.get('user')
    logedin_user = request.user.username

    # Retrieve the list of friends for each user
    current_user1 = FollowersCount.objects.all()
    logedin_user1 = FollowersCount.objects.all()

    # Find the intersection of the two sets
    mutual_friends = current_user1.intersection(logedin_user1)

    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_post' : user_post,
        'user_post_lenght' : user_post_lenght,
        'button_text' : button_text,
        'user_followers' : user_followers,
        'user_following' : user_following,
        'mutual_friends' : mutual_friends,
        }
    return render(request, 'account.html', context)

#for account settings
@login_required(login_url='signin')
def accounts_settings(request):
    user_profile = Profiles.objects.get(user=request.user)

    if request.method == 'POST' :

        if request.FILES.get('image') is not None:
            user_profile.profileimage = request.FILES['image']
        if 'bio' in request.POST:
            user_profile.bio = request.POST['bio']
        user_profile.save()

        return render(request,'account.html', {'user_profile': user_profile})
    return render(request, 'accounts_settings.html', {'user_profile': user_profile})

#for uploading posts
@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('upload_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
#for liking posts
@login_required(login_url='signin')
def like(request):
    userName = request.user.username
    postId = request.GET.get('post_id')

    post = Post.objects.get(id=postId)
    like_filter = LikePost.objects.filter(post_id=postId, username=userName).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=postId, username=userName)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')


# to create a new user
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 :
            if User.objects.filter(email = email).exists():
                messages.info(request, 'E mail already exist')
                return render(request, 'signup.html')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username already exist')
                return render(request, 'signup.html')
            else :
                user = User.objects.create_user(username = username, email=email, password=password)
                user.save()
                
                #create profile object
                user_model = User.objects.get(username  = username)
                new_profile = Profiles.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('/')
        else :
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else :
        return render(request, 'signup.html')
    

# for the login feature 
def signin(request):
    if request.method == 'POST' :
        usernameU = request.POST.get('username')
        passwordP = request.POST.get('password')

        user = auth.authenticate(username=usernameU, password=passwordP)

        if user is not None :
            auth.login(request, user)
            return redirect('/') 
        else :
            messages.info(request, 'Username or Password is unmatching')
            return redirect('signin') 
    else :
        return render(request, 'signin.html')
    
# for log out from the account
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin') 
