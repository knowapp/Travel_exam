from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages


def index(request):
    context = { 'user': User.objects.all() }
    return render(request, 'travelapp/index.html', context)


def login_page(request):
    #postData: user's postinfo
    postData = {
        'fullname' : request.POST['fullname'],
        'username' : request.POST['username'],
        'password' : request.POST['password'],
        'password_confirm' : request.POST['password_confirm'],
    }
    #to chekc errors and user info and use sessions 
    errors = User.objects.basic_validator(postData)
    if len(errors) ==0:

        request.session['id'] = User.objects.filter(username=postData['username'])[0].id
        request.session['fullname'] = postData['fullname']
        return redirect('/travel')
    else: 
        for errors in errors:
            messages.info(request, errors) 
        return redirect ('/')

def add(request):
    postData = {
		'destination' : request.POST['destination'],
		'start' : request.POST['start'],
		'end' : request.POST['end'],
		'plan' : request.POST['plan'],
		'join' : request.POST['join'],
    }
	return redirect('/travel') # Hi Anna, this one I need to work on... 


def login(request):
    postData = {

    'username' : request.POST['username'],
    'password' : request.POST['password']
    
    }
    #error handler checks user input
    errors = User.objects.login(postData)
    #if theres no errors
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(username=postData['username'])[0].id
        request.session['fullname'] = User.objects.filter(username=postData['username'])[0].username
        return redirect('/')
    for errors in errors:
        messages.info(request, errors)
    return redirect('/travel')

def travel(request):
    context = {
        'user': User.objects.all(),
        # 'travel': Travel.objects.all() #Anna, I almost made it.. 
    }
    return render(request, 'travelapp/travel.html', context)


def logout(request):
    #delte id
    del request.session['id']
    del request.session['fullname']

    return redirect('/')
