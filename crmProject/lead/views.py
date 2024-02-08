import csv

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView


from .forms import AddCommentForm, AddFileForm
from .models import Lead

from client.models import Client, Comment as ClientComment
from team.models import Team


@login_required
def leads_export(request):
    leads = Lead.objects.filter(created_by = request.user)
    
    response = HttpResponse(
        content_type = "text/csv",
        headers = {"Content-Disposition": "attachment ; filename = 'leads.csv'"},
    )
    
    writer = csv.writer(response)
    writer.writerow(["Leads", "Email", "Description", "Created by", "Created at"])
    
    for lead in leads:
        writer.writerow([lead.name, lead.email, lead.description, lead.created_by, lead.created_at])
    
    return response

# Class based view
class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

    
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by = self.request.user, converted_to_client = False)



class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    
    # Comment and File section view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddCommentForm()
        context["fileform"] = AddFileForm()
        return context
    
    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by = self.request.user, pk = self.kwargs.get("pk"))



class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy("leads:list")
    
    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        messages.success(self.request, "The lead was deleted.")
        return queryset.filter(created_by = self.request.user, pk = self.kwargs.get("pk"))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    fields = ("name", "email", "description", "priority", "status", )
    success_url = reverse_lazy("leads:list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Lead"
        return context

    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by = self.request.user, pk = self.kwargs.get("pk"))
    
    

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    fields = ("name", "email", "description", "priority", "status", )
    success_url = reverse_lazy("leads:list") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by = self.request.user)[0]
        context["team"] = team
        context["title"] = "Add Lead"
        return context

    def form_valid(self, form):
        team = Team.objects.filter(created_by = self.request.user)[0]
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()
        messages.success(self.request, "The lead was created.")
        return redirect(self.get_success_url())
            


class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            team = Team.objects.filter(created_by = self.request.user)[0]
            file = form.save(commit=False)
            file.team = team
            file.created_by = request.user
            file.lead_id = pk
            file.save()
            
        return redirect("leads:detail", pk = pk)

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        form = AddFileForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by = self.request.user)[0]
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
            
        return redirect("leads:detail", pk = pk)
        

class ConvertToClientView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        lead = get_object_or_404(Lead, created_by = request.user, pk = pk)
        team = Team.objects.filter(created_by = request.user)[0]
        client = Client.objects.create(
            name = lead.name,
            email = lead.email,
            description = lead.description,
            created_by = request.user,
            team = team,
        )
        
        lead.converted_to_client = True
        lead.save()
        
        # convert lead comments to client comments
        comments = lead.comments.all()
        for comment in comments:
            ClientComment.objects.create(
                client = client,
                content = comment.content,
                created_by = comment.created_by,
                team = team
            )
            
        # Show the success message and redirect
        messages.success(request, "The lead was converted to a client.")
        return redirect("leads:list")
