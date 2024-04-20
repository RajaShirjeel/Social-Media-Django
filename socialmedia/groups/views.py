from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import mixins
from django.views import generic
from django.urls import reverse

from . import models
# Create your views here.
class CreateGroup(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Group
    fields = ('name', 'description')

class ListGroups(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Group
    
class SingleGroup(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Group

class JoinGroup(mixins.LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, *args, **kwargs):
        group = get_object_or_404(models.Group, slug = self.kwargs.get('slug'))
        
        try:
            models.GroupMember.objects.create(user=self.request.user, group=group)
        
        except:
            messages.warning(self.request, "Already a member of this group!")
        
        else:
            messages.success(self.request, "Group joined Successfully!")
        
        return super().get(self, *args, **kwargs)

class LeaveGroup(mixins.LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})
    
    def get(self, *args, **kwargs):
        try:
            member = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        
        except:
            messages.warning(self.request, 'Not a member of this group!')
        
        else:
            member.delete()
            messages.warning(self.request, 'Group Left!')
        
        return super().get(self, *args, **kwargs)
    