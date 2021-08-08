from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from account.decorators import *
from django.contrib.auth.mixins import LoginRequiredMixin




@login_required(login_url='/')
#@allowed_users(allowed_roles=['admin'])
def home(request):
    k = 0
    model = Projet.objects.filter(user=request.user)
    for i in model:
        k = k+1

    context = {
        "nbre": k,
    }

    return render(request, 'site/home.html', context)




class AddProjet(LoginRequiredMixin,CreateView):
    model = Projet
    form_class = CreateProjetForm
    template_name = "projet/create_projet.html"
    success_url = "/projet/"
    raise_exception = True

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class projet_list_view(LoginRequiredMixin,ListView):
    template_name = "projet/projets.html"
    model = Projet
    paginate_by = 100
    raise_exception = True


    def get_queryset(self):
        return Projet.objects.filter(user=self.request.user) #to display infos based on users



class UpdateProjet(LoginRequiredMixin, UpdateView):
    template_name = "projet/update_projet.html"
    model = Projet
    form_class = CreateProjetForm
    success_url = "/projet/"
    raise_exception = True


class DeleteProjet(LoginRequiredMixin, DeleteView):
    model = Projet
    template_name = "projet/delete_projet.html"
    success_url = reverse_lazy('projet:home')
    raise_exception = True




