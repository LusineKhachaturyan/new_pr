from asyncore import write
import csv
import datetime

from dataclasses import fields
from distutils.command.clean import clean
from multiprocessing import context
from tempfile import template
from urllib import response
from django.conf import settings
from django.shortcuts import render, redirect
from service.models import Post, Comment
from .forms import MessageForm
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage 
from django.http import HttpResponse

def index(req):
    return render(req, 'index.html')

@login_required
@permission_required('service.view_post')

def about(req):
    form = MessageForm()
    if req.method == "POST":
       form = MessageForm(req.POST)
       if form.is_valid():
           subject = form.cleaned_data.get('title')
           body = form.cleaned_data.get('body')
           try:
                send_mail(subject, body, settings.EMAIL_HOST_USER, ['jamoca9099@nuesond.com'], fail_silently=False)
                form.save()
           except Exception as err:
                print(str(err))
           return redirect('about')
    return render(req, 'about.html', {'form':form})

class RegisterForm(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    success_message = '{%username%} was created successfully'
    template_name  = 'register.html'
    success_url = reverse_lazy('login')

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

class DetailPostView(DetailView):
    model = Post
    template_name = 'detail_post.html'

class CreatePostView(CreateView):
    model = Post
    template_name = 'create_post.html' 
    fields = "__all__"
    ordering = ["pk"]

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'create_post.html'
    fields = "__all__"

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy("index")

class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    fields = "__all__"

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
 
def upload(req):
    context= {}
    if req.method == "POST":
        upload_file = req.FILES['file']
        file = FileSystemStorage 
        name = file.save(upload_file.name, upload_file)
        context['url'] = file.url(name)
    return render(req, 'upload.html', context)
    

def download(req):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Create_at'])
    for row in Post.objects.all().values_list('title', 'description', 'create_at'):
        writer.writerow(row)
    #filename = str(datetime.datetime.now{})
    response['Content-Disposition'] = "attachment; filename= 'post.csv"
    return response