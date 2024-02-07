import csv

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AddClientForm, AddCommentForm, AddFileForm
from .models import Client

from team.models import Team


@login_required
def clients_export(request):
    clients = Client.objects.filter(created_by = request.user)
    
    response = HttpResponse(
        content_type = "text/csv",
        headers = {"Content-Disposition": "attachment ; filename = 'clients.csv'"},
    )
    
    writer = csv.writer(response)
    writer.writerow(["Client", "Email", "Description", "Created by", "Created at"])
    
    for client in clients:
        writer.writerow([client.name, client.email, client.description, client.created_by, client.created_at])
    
    return response

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by = request.user)
    
    return render(request, "client/clients_list.html", {
        "clients": clients
    })
    # return render(request, "client/clients:list.html")

@login_required
def clients_add_file(request, pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)
    team = Team.objects.filter(created_by = request.user)[0]
    
    if request.method == "POST":
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.team = team
            file.created_by = request.user
            file.client_id = pk
            file.save()
            
            return redirect("clients:detail", pk = pk)
    return redirect("clients:detail", pk = pk)

@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)
    # client = client.objects.filter(created_by=request.user).get(pk = pk)
    team = Team.objects.filter(created_by = request.user)[0]
    
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client
            comment.save()
            
            return redirect("clients:detail", pk = pk)
    else:
        form = AddCommentForm()
    
    return render(request, "client/clients_detail.html", {
        "client": client,
        "form": form,
        "fileform": AddFileForm(),
    })
    
@login_required
def clients_add(request):
    team = Team.objects.filter(created_by = request.user)[0]
    
    if request.method == "POST":
        form = AddClientForm(request.POST)
        
        if form.is_valid():
            team = Team.objects.filter(created_by = request.user)[0]
            # Prevent from comitting to the db before we add the user
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            
            messages.success(request, "The client was created.")
            
            return redirect("clients:list")
    else:
        form = AddClientForm()
        
    return render(request, "client/clients_add.html",{
        "form": form,
        "team": team,
    })
    
@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)
    if request.method == "POST":
        form = AddClientForm(request.POST, instance = client)

        if form.is_valid():
            form.save()

            messages.success(request, "The changes were saved.")
            
            return redirect("clients:list")
        
    else:
        form = AddClientForm(instance = client)
        
    return render(request, "client/clients_edit.html",{
        "form": form
    })
    
@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, created_by = request.user, pk = pk)
    client.delete()
    
    messages.success(request, "The client was deleted.")
    
    return redirect("clients:list")