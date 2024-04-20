from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.http import Http404
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render
from django.views import generic
from django.contrib.auth import mixins
from django.urls import reverse_lazy
from . import models
from groups.models import Group, GroupMember
# Create your views here.
User = get_user_model()
class PostList(generic.ListView, SelectRelatedMixin):
    model = models.Post
    select_related = ('user', 'group')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            user_group_ids = GroupMember.objects.filter(user=self.request.user).values_list('group', flat=True)
            user_group_ids = list(user_group_ids)
            user_groups = Group.objects.filter(pk__in=user_group_ids)
            all_groups = Group.objects.all()
            user_posts = models.Post.objects.filter(user=self.request.user)
            context['user_groups'] = user_groups
            context['all_groups'] = all_groups
            context['user_posts'] = user_posts

        return context


class CreatePost(generic.CreateView, mixins.LoginRequiredMixin, SelectRelatedMixin):
    model = models.Post
    fields = ('message', 'group')
    success_url = reverse_lazy('posts:all')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostDetail(generic.DetailView, SelectRelatedMixin):
    model = models.Post
    select_related = ('post', 'group')

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class UserPosts(generic.ListView):
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404('User does not exist')
        else:
            self.post_user.posts.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = models.Post.objects.filter(user=self.request.user)
        context['post_user'] = self.post_user
        context['post_list'] = user_posts
        return context


class DeletePost(generic.DeleteView, mixins.LoginRequiredMixin, SelectRelatedMixin):
    model = models.Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleting_post'] = True
        return context
    