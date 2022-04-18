from email import message
from fnmatch import fnmatchcase
import imp
from django.conf import Settings, settings
from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from Authentication import settings

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

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
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try anothee Username")
            return redirect('home')



        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "Username must be under 10 character")

        if pass1 != pass2:
            messages.error(request, "Password Didn't Matched")
            
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        
        myuser.save()
        
        messages.success(request, "Your Account has been Successfullt created")
        
        
        #Welcome email
        
        subject = "Welcome to this website"
        message = "Hello " + myuser.first_name + "welcome.\n Thank you for visiting our website. \n We have sent you an confirmation email, please confirm to activate"
        from_email = settings.EMAIL_HOST_USER
        to_list = myuser.email
        send_mail(subject, from_email, to_list, fail_silently=True)
        
        
        #Email Address Confirmation Email
        
        current_site = get_current_site(request)
        email_subject = "Confirm your email"
        message2 = render_to_string('email_confirmation.html'), {
            'name' : myuser.first_name,
            'domain' : current_site.domain,
            
        }
        
        return redirect('signin')
        
        
        
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


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return render(request, 'authenticate/logout.html')


