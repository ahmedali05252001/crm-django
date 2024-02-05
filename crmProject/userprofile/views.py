from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .models import Userprofile

from team.models import Team

def signup(request):
    if request.method == 'POST':                #if we have a POST request
        form = UserCreationForm(request.POST)           #if we try to submitt the form
        if form.is_valid():
            user = form.save()      #if the form is correct then create the user and the userprofile
            Userprofile.objects.create(user = user)
            
            team = Team.objects.create(name = "The team name", created_by = request.user)
            team.members.add(request.user)
            team.save()
            
            return redirect('/log-in/')
    else:                                       #if we have a GET request
        form = UserCreationForm()
    return render(request, 'userprofile/signup.html',{
        'form': form
    })

@login_required
def myaccount(request):
    team = Team.objects.filter(created_by = request.user)[0]
    return render(request, "userprofile/myaccount.html",{
        "team": team
    })
