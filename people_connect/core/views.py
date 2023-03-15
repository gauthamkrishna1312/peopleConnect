from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profiles

# Create your views here.

#to call home page
def index(request):
    return render(request, 'index.html')

#to call a page for dev purpose
def blank(request):
    return render(request, 'index.html')

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

                # Log on to profile page

                #create profile object
                user_model = User.objects.get(username  = username)
                new_profile = Profiles.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('blank')
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
def logout(request):
    auth.logout(request)
    return redirect('signin') 
