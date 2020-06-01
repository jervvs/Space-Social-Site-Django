from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404

#what is braces for? SelectRelatedMixin can be used to
from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    #can see what's the point of get_context_data
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model= models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin,generic.CreateView):
    fields = ('message','group')
    model = models.Post
    redirect_field_name = 'posts/post_list.html'
    form_class = forms.PostForm

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.username
        self.object.save() #connects actual post to user itself
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related=('user','group')
    success_url = reverse_lazy('posts:all') #when you have successfully deleted the posts

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
