from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post 
# Create your views here.

def bloghome(request):
    allPosts = Post.objects.filter(status='Approved')
   
    context = {'allPosts' : allPosts}
    return render(request,'blog/home.html',context)


def blogPost(request, slug): 
    post = Post.objects.filter(slug=slug).first() 
    context = {'post' : post}    
    return render(request,'blog/blogpost.html',context)



