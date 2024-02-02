from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .models import Userprofile

def signup(request):
    if request.method == 'POST':                #if we have a POST request
        form = UserCreationForm(request.POST)           #if we try to submitt the form
        if form.is_valid():
            user = form.save()      #if the form is correct then create the user and the userprofile
            Userprofile.objects.create(user = user)
            
            return redirect('/log-in/')
    else:                                       #if we have a GET request
        form = UserCreationForm()
    return render(request, 'userprofile/signup.html',{
        'form': form
    })


