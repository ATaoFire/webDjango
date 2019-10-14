from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Banner,Post,BlogCategory,Tags,Comment,FriendlyLink
#实现搜索

from django.views.generic.base import View
from django.db.models import Q
#分页机制
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class SearchView(View):
    # def get(self, request):
    #     pass
    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw)|Q(content__icontains=kw))

        ctx = {
            'post_list': post_list
        }
        return render(request, 'list.html', ctx)
# 视图函数 HTTPRequest
def index(request):
    banner_list = Banner.objects.all()
    recommend_list = Post.objects.filter(recommend=1)
    post_list = Post.objects.order_by('-pub_date').all()[:10]
    blogcategory_list = BlogCategory.objects.all()
    new_comment_list = Comment.objects.all()
    friendlylink_list = FriendlyLink.objects.all()

    ctx = {
        'banner_list': banner_list,
        'recommend_list': recommend_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'new_comment_list':new_comment_list,
    }
    return render(request, 'index.html',  ctx)


class TagMessage(object):
    def __init__(self, tid, name, count):
        self.tid = tid
        self.name = name
        self.count = count

def blog_list(request):
    post_list = Post.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(post_list, per_page=1, request=request)

    post_list = p.page(page)

    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)

    ctx = {
        'post_list': post_list,
        'tags': tag_message_list
    }
    return render(request, 'list.html', ctx)