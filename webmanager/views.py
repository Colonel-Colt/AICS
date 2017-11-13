# coding: UTF-8
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
import os

from django.contrib.auth.decorators import login_required


from .forms import UserForm


#register
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #get form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Is user exist?
            user = auth.authenticate(username = username,password = password)
            if user:
                context['userExit']=True
                return render(req, 'register.html', context)


            #Add user to the database
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #Add session
            req.session['username'] = username

            auth.login(req, user)
            #redirect
            return redirect('/')
    else:
        context = {'isLogin':False}
    #return context
    return  render(req,'register.html',context)

#Login


def login_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #Get password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #Ask database
            user = authenticate(username = username,password = password)
            if user:
                #redirect index
                auth.login(req,user)
                req.session['username'] = username
                return redirect('upload')
            else:
                #fail, stay login
                context = {'isLogin': False, 'pswd':False}
                return render(req, 'login.html', context)
    else:
        context = {'isLogin': False,'pswd':True}
    return render(req, 'login.html', context)


#Logout
def logout_view(req):
    #Clear cookies
    auth.logout(req)
    return redirect('/')

def upload_view(req):
    context = {}
    if req.method == "POST":# If post, run
        train = req.FILES.get("train", None)  #Get the file
        if not train:
            context = {'isUpload': False}
            return render(req, 'upload.html', context)
        destination = open(os.path.join("/../temp/",train.name),'wb+')
                #write
        for chunk in train.chunks():
                #each chunk
            destination.write(chunk)
            destination.close()
            context = {'isUpload': True}
        return render(req, 'upload.html', context)
    else:
        context = {'isUpload': False}
    return render(req, 'upload.html', context);