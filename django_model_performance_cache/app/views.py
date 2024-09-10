from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.core.cache import cache


def post_list(request):
    posts = Post.objects.all()
    cache_key = Post.get_cache_key()
    cache_used = cache.get(cache_key) is not None
    return render(request, "blog/post_list.html", {"posts": posts})


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})
