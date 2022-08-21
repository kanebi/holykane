from unicodedata import category
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
# Create your views here.
from .models import BlogPost, Category, Comment
from django.contrib import messages


def index(request):
    context = {
        'blogs': BlogPost.objects.all().order_by('-created_on')
    }
    return render(request, 'blog/index.html', context)


def blogDetail(request, date, slug):
    blog = get_object_or_404(BlogPost, created_on__date=date, slug=slug)
    context = {
        'blog': blog,
        'related_blog': BlogPost.objects.filter(Q(title=blog.title) | Q(tags__name__contains=blog.tags) | Q(category=blog.category) | Q(keywords__in=blog.keywords)),
        'categories': Category.objects.all()
    }
    return render(request, 'blog/blog-detail.html', context)


def byCategory(request, title):
    blogPosts = BlogPost.objects.all().filter(category__title=title)
    context = {
        'blogPosts': blogPosts,
        'categories': Category.objects.all()
    }
    return render(request, 'blog/blog-detail.html', context)


def add_comment(request, blog_id):
    if request.method == 'POST':
        comment = Comment()
        print(request.POST)
        blog = get_object_or_404(BlogPost, id=blog_id)
        if str(request.POST.get('comment_parent')).isnumeric():
            commentId = request.POST.get('comment_parent')
            targetcomment = get_object_or_404(Comment, id=commentId)
            if not request.user.is_authenticated:
                comment.name = request.POST.get('name')
                comment.comment = request.POST.get('comment')
                comment.email = request.POST.get('email')
                comment.post = blog

                comment.save()

            else:
                comment.user = request.user
                comment.comment = request.POST.get('comment')
                comment.name = request.user.username
                comment.email = request.user.email
                comment.post = blog

                comment.save()

            targetcomment.replies.add(comment)
            messages.success(request, 'Comment replied', extra_tags='success')

        else:
            if not request.user.is_authenticated:
                comment.name = request.POST.get('name')
                comment.comment = request.POST.get('comment')
                comment.email = request.POST.get('email')
                comment.post = blog
                comment.save()
            else:
                comment.user = request.user

                comment.comment = request.POST.get('comment')
                comment.name = request.user.username
                comment.email = request.user.email
                comment.post = blog
                comment.save()
                messages.success(request, 'Comment Posted',
                                 extra_tags='success')
    return redirect(blog.get_absolute_url())
