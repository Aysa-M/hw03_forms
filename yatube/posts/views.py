from django.contrib.auth import login
from core.templatetags.user_filters import authorized_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


@login_required
def index(request):
    """Information which is showing up on the start page."""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


@authorized_only
def group_posts(request, slug):
    """Information for displaying on the page with posts grouped by GROUPS."""
    group = get_object_or_404(Group, slug=slug)
    post_list_group = Post.objects.filter(group=group).all()
    paginator_group = Paginator(post_list_group, 10)
    page_number_group = request.GET.get('page')
    page_obj = paginator_group.get_page(page_number_group)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@authorized_only
def profile(request, username):
    """
    The view shows a page profile of an authorised user.
    """
    user = get_object_or_404(User, username=username)
    post_list_profile = Post.objects.filter(author=user).all()
    paginator_profile = Paginator(post_list_profile, 10)
    page_number_profile = request.GET.get('page')
    page_obj = paginator_profile.get_page(page_number_profile)
    post_quantity = post_list_profile.count()
    context = {
        'user': user,
        'page_obj': page_obj,
        'post_quantity': post_quantity,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """The view shows information about a current post."""
    post_profile = get_object_or_404(Post, pk=post_id)
    title = post_profile.text[:30]
    context = {
        'post_profile': post_profile,
        'title': title,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """The view creates a new post by a special form."""
    form = PostForm()
    groups = Group.objects.all()
    context = {
        'form': form,
        'groups': groups,
    }
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """
    This view edits the post by its id and saves changes in database.
    """
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
    groups = Group.objects.all()
    is_edit = True
    context = {
        'form': form,
        'is_edit': is_edit,
        'groups': groups,
    }
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if post.author != request.user:
            return redirect('posts:post_detail', pk=post_id)
        elif post.author == request.user:
            if form.is_valid():
                post.author = request.user
                post.pk = post_id
                post.text = form.cleaned_data['text']
                post.save()
                return redirect('posts:post_detail', pk=post_id)
        else:
            PostForm(instance=post)
            return redirect('posts/create_post.html')
    return render(request, 'posts/create_post.html', context)
