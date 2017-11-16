# coding: UTF-8
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, render_to_response
import os
import time
import random
import sys
from django.contrib.auth.decorators import login_required

#from CV import trainCNN
#from CV import trainSVM

from .forms import UserForm


def app_view(req):
    context = {}
    if req.method == 'GET':
        username = req.GET['name']
        modelpath = os.getcwd() + "/user/" + username + "/cnn.model"
        if not os.path.exists(modelpath):
            modelpath = os.getcwd() + "/user/" + username + "/svm.model"
            if not os.path.exists(modelpath):
                return render(req, "error.html", context)
        context = {'username': username}
        return render(req, "app.html", context)
    if req.method == 'POST':
        srcimg = req.FILES.get("image-file", None)
        s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        srcname = "".join(random.sample(s, 12))
        try:
            srcpath = open(os.path.join(os.getcwd() + "/temp/", srcname), 'wb')
            for chunk in srcimg.chunks():
                srcpath.write(chunk)
            srcpath.close()
        except IOError, e:
            srcpath = os.path.join(os.getcwd() + "/temp/", srcname)
        username = req.GET['name']
        modelpath = os.getcwd() + "/user/" + username + "/cnn.model"
        if not os.path.exists(modelpath):
            modelpath = os.getcwd() + "/user/" + username + "/svm.model"
            if not os.path.exists(modelpath):
                return render(req, "error.html", context)
            #result = runSVM.run(username, [srcpath])[0]
            #
        #result = runCNN.run(username, [srcpath])[0]



        return render(req, "result.html", context)


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

            path = os.getcwd() + "/user/" + username + "/training_set/"
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.getcwd() + "/user/" + username + "/app/"
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.getcwd() + "/user/" + username + "/temp/"
            if not os.path.exists(path):
                os.makedirs(path)
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
            user = authenticate(username = username, password = password)
            if user:
                #redirect index
                auth.login(req,user)
                req.session['username'] = username
                return redirect('select')
            else:
                #fail, stay login
                context = {'isLogin': False, 'pswd':False}
                return render(req, 'login.html', context)
    else:
        if req.user.is_authenticated():
            return redirect('select')
        context = {'isLogin': False,'pswd':True}
    return render(req, 'login.html', context)


#Logout
def logout_view(req):
    #Clear cookies
    auth.logout(req)
    return redirect('/')


@login_required
def select_view(req):
    context = {}
    if req.method == 'POST':
        if req.POST.has_key('SVM'):
            redirect('upload_svm')
            return render(req, 'upload_svm.html', context)
        else:
            redirect('upload_cnn')
            return render(req, 'upload_cnn.html', context)
    else:
        context = {'isChosen': False}
        return render(req, 'select.html', context)


@login_required
def upload_cnn_view(req):
    context = {}
    if req.method == "POST":
        train = req.FILES.get("train", None)
        if not train:
            context = {'isUpload': False}
            return render(req, 'upload_cnn.html', context)
        try:
            destination = open(os.path.join(os.getcwd() + "/user/" + req.user.username + "/", "input.txt"), 'wb')
            for chunk in train.chunks():
                destination.write(chunk)
            destination.close()
            context = {'isUpload': True, 'filePath': destination, 'type': 'CNN'}
        except IOError, e:
            destination = os.path.join(os.getcwd() + "/user/" + req.user.username + "/", "input.txt")
        context = {'isUpload': True}
        time.sleep(10);
        #classes = ["0", "1"]
        #result = trainCNN.trainCNN("/home/ubuntu/data/mnist_png/training", classes, 28,"/home/ubuntu/aics_temp/"+req.session["username"]+".model")
        return render_to_response('success.html', context)
    else:
        context = {'isUpload': False}
    return render(req, 'upload_cnn.html', context);


@login_required
def upload_svm_view(req):
    context = {}
    if req.method == "POST":
        train = req.FILES.get("train", None)
        if not train:
            context = {'isUpload': False}
            return render(req, 'upload_svm.html', context)
        try:
            destination = open(os.path.join(os.getcwd() + "/user/" + req.user.username + "/", "input.txt"), 'wb')
            for chunk in train.chunks():
                destination.write(chunk)
            destination.close()
            context = {'isUpload': True, 'filePath': destination, 'type': 'SVM'}
        except IOError, e:
            destination = os.path.join(os.getcwd() + "/user/" + req.user.username + "/", "input.txt")
        time.sleep(10);
        #classes = ["0", "1"]
        #result = trainSVM.trainSVM("/home/ubuntu/data/mnist_png/training", classes, 28,"/home/ubuntu/aics_temp/"+req.session["username"]+".model")
        return render_to_response('success.html', context)
    else:
        context = {'isUpload': False}
    return render(req, 'upload_svm.html', context);
