from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .forms import PostFrom
from .filters import PostFilter

from .models import Post

def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]

    context = {'posts' :posts}
    return render( request, 'base/index.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET ,queryset=posts)
    posts=myFilter.queryset

    page =request.GET.get('page')

    paginator = Paginator(posts, 3)

    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage: 
        posts =paginator.page(paginator.num_pages)


    context = {'posts' :posts,  'myFilter'  :myFilter }
    return render(request, 'base/posts.html',context)

def post(request, slug):
    post = Post.objects.get(slug=slug)

    context = {'posts' :post}
    return render(request, 'base/post.html', context)

def profile(request):
    return render(request, 'base/profile.html')


#crud views

@login_required(login_url='home')
def createPost(request):
    form = PostFrom()

    if request.method =='POST':
        form = PostFrom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('Posts')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url='home')
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostFrom(instance=post)

    if request.method =='POST':
        form = PostFrom(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('Posts')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url='home')
def deletPost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method =='POST':
       post.delete()
       return redirect('Posts')

    context = {'item': post}
    return render(request, 'base/delete.html', context)


def sendEmail(request):

    if request.method =='POST' :

        template = render_to_string('base/email_template.html', {
            'name':request.POST['name'],
            'email' :request.POST['email'],
            'message' :request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['rantir570@gmail.com']
            )
        email.fail_silently=False
        Email.send()
    return render(request, 'base/email_sent.html')