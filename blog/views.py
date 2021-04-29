from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, PostComment
from .forms import SignUpForm


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class blogListView(ListView):
    model = Post
    template_name = "home.html"

class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        post = Post.objects.all()
        #context['sidebar_articles'] = Post.order_by('-created')[:15]
        return context


class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ['title', 'author', 'body']

class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")

class CreatePostComment(CreateView):
    model = PostComment
    fields = ('text',)

    def post_valid(self, form):
        post = get_object_or_404(Post,
                                    slug=Post.slug) # Replaced 'Post' with 'Article'
        article = post.objects.all()
        articlecomment = form.save(commit=False)
        articlecomment.author = self.request.user
        articlecomment.article = Post
        articlecomment.save()
        return redirect('post_detail', slug=article.slug)

    def get_success_url(self):
        return reverse_lazy('home')
