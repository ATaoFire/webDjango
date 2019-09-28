from django.shortcuts import render, get_object_or_404
from .models import Post
#分页机制
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    posts = Post.objects.all().exclude(status__regex='draft')
    # paginator = Paginator(object_list, 1)
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     # 如果「不是数字」则去第一页
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     # 如果「页数太大」就去最后一页
    #     posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/home.html',
                  {'posts': posts})
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
# def home(request):
#     return render(request, 'blog/home.html')
#
# def login(request):
#     return render(request, 'blog/login.html')
#
# def register(request):
#     return render(request, 'blog/register.html')