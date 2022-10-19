from django.core.paginator import Paginator

from django.contrib.auth.decorators import user_passes_test, \
    REDIRECT_FIELD_NAME

from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User

from .forms import PostForm


def login_required(
        function=None,
        redirect_field_name=REDIRECT_FIELD_NAME,
        login_url=None
):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    number_posts = Post.objects.filter(author=author).count()
    post_list = Post.objects.filter(author=author).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
        'number_posts': number_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post_info = get_object_or_404(Post, pk=post_id)
    post_id = post_id
    author_posts = post_info.author
    author_count = post_info.author.posts.count()

    context = {
        'post_info': post_info,
        'author_posts': author_posts,
        'author_count': author_count,
        'post_id': post_id
    }
    return render(request, 'posts/post_detail.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


@login_required
@csrf_protect
def post_create(request):
    template = 'posts/create_post.html'
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # form.save(author_id=user.id)
            return redirect('posts:profile', user.username)
    else:
        form = PostForm()
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = Post.objects.get(pk=post_id)
    if request.user == post.author:
        form = PostForm(request.POST or None, instance=post)
        context = {
            'form': form,
            'is_edit': True,
        }
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
        return render(request, template, context)
    return redirect('posts:post_detail', post_id)
