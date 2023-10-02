from asyncio.windows_events import NULL
from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from blogpost import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
#from . tokens import generate_token
# Create your views here.

@csrf_exempt
def admin_home(request):
      allPosts = Post.objects.filter(status='Waiting')
      context = {'allPosts' : allPosts}
      return render(request,'admin_use/home.html',context)

@csrf_exempt
def allblogs(request):
      allPosts = Post.objects.all()
      context = {'allPosts' : allPosts}
      return render(request,'admin_use/allblogs.html',context)


@csrf_exempt
def signin(request):
      if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            allPosts = Post.objects.filter(status='Waiting')
            context = {'allPosts' : allPosts}
            return render(request,'admin_use/home.html',context)
            # messages.success(request, "Logged In Sucessfully!!")
            
        else:
            messages.error(request, "Bad Credentials!!")
            return render(request, "admin_use/login.html")
    
      return render(request, "admin_use/login.html")

@csrf_exempt
def blogPost(request, slug): 
      post = Post.objects.filter(slug=slug).first() 
      context = {'post' : post}  

      if post != NULL:  
            return render(request,'admin_use/blogpost.html',context)

      else:
            allPosts = Post.objects.filter(status='Waiting')
            context = {'allPosts' : allPosts}
            return render(request,'admin_use/home.html',context) 


def allblogs_blogpost(request,slug):
      post = Post.objects.filter(slug=slug).first() 
      context = {'post' : post}  

      if post != NULL:  
            return render(request,'admin_use/allblog_blogpost.html',context)

      else:
            allPosts = Post.objects.filter(status='Waiting')
            context = {'allPosts' : allPosts}
            return render(request,'admin_use/home.html',context) 


@csrf_exempt
def blog_accept(request , slug):
      post = Post.objects.filter(slug=slug).first() 
      post.status = "Approved"
      post.save() 
     
      
      return redirect('admin_home')


@csrf_exempt
def blog_decline(request , slug):
      post = Post.objects.filter(slug=slug).first() 
      post.status = "Decline"
      post.save() 
     
     
      return redirect('admin_home')


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return render(request,'admin_use/createuser.html') 
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return render(request,'admin_use/createuser.html') 
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            allPosts = Post.objects.filter(status='Waiting')
            context = {'allPosts' : allPosts}
            return render(request,'admin_use/createuser.html')  
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            allPosts = Post.objects.filter(status='Waiting')
            context = {'allPosts' : allPosts}
            return render(request,'admin_use/createuser.html') 
        
       
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check mail for confirmation")
        
        # Welcome Email
        subject = "Welcome to Cnet Family !!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Cnet!! \nNow you can login to your account and upload blogs \n\nThanking You\nHet"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
  
        return render(request,'admin_use/createuser.html') 
        
        
    return render(request,'admin_use/createuser.html') 



@csrf_exempt
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')