from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from account.decorators import *



@login_required(login_url='/')
#@allowed_users(allowed_roles=['admin'])
def home(request):
    context = {}
    return render(request, 'home.html', context)



class AddProjet(CreateView):
    model = Projet
    form_class = CreateProjetForm
    template_name = "projet/create_projet.html"
    success_url = "/projet/"

    @login_required(login_url='/')
    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        # do something with self.object
        return HttpResponseRedirect(self.get_success_url())


class projet_list_view(ListView):
    template_name = "projet/projets.html"
    model = Projet
    paginate_by = 100

    @login_required(login_url='/')
    def get_queryset(self):
        return Projet.objects.filter(user=self.request.user) #to display infos based on users



class UpdateProjet(UpdateView):
    template_name = "projet/update_projet.html"
    model = Projet
    form_class = CreateProjetForm
    success_url = "/projet/"


class DeleteProjet(DeleteView):
    model = Projet
    template_name = "projet/delete_projet.html"
    success_url = reverse_lazy('projet:home')




