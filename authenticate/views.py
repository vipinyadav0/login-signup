from fnmatch import fnmatchcase
import imp
from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'authenticate/base.html')

def signup(request):
    if request.method == 'POST':
        # username = request.POST.get("username") or 
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        myuser = User.objects.create_user(username, email, pass1)
        
        myuser.first_name = fname
        myuser.last_name = fname
        
        myuser.save()
        
        messages.success(request, "Your Account has been Successfullt registered")
        
        return redirect('login')
        
        
        
    return render(request, 'authenticate/signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
    
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user) 
            fname = user.first_name
            return render(request, "authenticate/base.html", {'fname': fname})
            
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('home')
        
        
        
    return render(request, 'authenticate/signin.html')


def logout(request):
    return render(request, 'authenticate/logout.html')


