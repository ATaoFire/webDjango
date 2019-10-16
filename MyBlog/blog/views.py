from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect,reverse
from blog.models import BlogUser,Banner,Post,BlogCategory,Tags,Comment,FriendlyLink
from datetime import datetime
#实现搜索
from django.views.generic.base import View
from django.db.models import Q
#分页机制
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#登录
from django.contrib.auth import authenticate, login, logout
#注册
from django.contrib.auth.hashers import make_password
#邮箱发邮件
from random import Random
from django.core.mail import send_mail
from .models import EmailVerifyRecord
from MyBlog.settings import EMAIL_FROM


# 生成随机字符串
def make_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送邮件
def my_send_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = make_random_str(4)
    else:
        code = make_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "知奇博客-注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "知奇博客-网注册密码重置链接"
        email_body = "请点击下面的链接重置密码: http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "知奇博客-邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = BlogUser.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, 'login.html', {'error_msg':'用户未激活！'})
        else:
            return render(request, 'login.html', {'error_msg':'用户名或者密码错误！'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # my_send_email(email)

        user = BlogUser()
        user.username = username
        user.password = make_password(password)
        user.email = email
        user.is_active = False

        user.save()

        return render(request, 'login.html', {})

class SearchView(View):
    # def get(self, request):
    #     pass
    def post(self, request):
        kw = request.POST.get('keyword')

        if kw:
            post_list = Post.objects.filter(Q(title__icontains=kw)|Q(content__icontains=kw))
            ctx = {
                'post_list': post_list
            }
            return render(request, 'list.html', ctx)
        else:
            return render(request, 'list.html', {})


# 视图函数 HTTPRequest
def index(request):
    banner_list = Banner.objects.all()
    recommend_list = Post.objects.filter(recommend=1)
    post_list = Post.objects.order_by('-pub_date').all()[:10]

    blogcategory_list = BlogCategory.objects.all()
    #进行去重，过滤
    new_comment_list = Comment.objects.all()
    new_comment_list1 = []
    post_list1 = []
    for comment in new_comment_list:
        if comment.post.id not in post_list1:
            new_comment_list1.append(comment)
            post_list1.append(comment.post.id)

    friendlylink_list = FriendlyLink.objects.all()
    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)

    ctx = {
        'banner_list': banner_list,
        'recommend_list': recommend_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'new_comment_list': new_comment_list1,
        'friendlylink_list':friendlylink_list,
        'tags': tag_message_list,
    }
    return render(request, 'index.html',  ctx)


class TagMessage(object):
    def __init__(self, tid, name, count):
        self.tid = tid
        self.name = name
        self.count = count

def blog_list(request,cid=-1, tid=-1):

    """
    分页器的使用
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10)
    print("count:", paginator.count)  # 总数居
    print("num_pages", paginator.num_pages)  # 总页数
    print("page_range", paginator.page_range)  # 页面的列表

    page_one = paginator.page(1)  # 第一页的page对象
    for i in range(page_one):  # 遍历第1页的所有数据对象
        print(i)
    print(page_one.object_list)  # 第1页所有数据

    page_two = paginator.page(2)
    print(page_two.has_next())  # 是否有下一页
    print(page_two.next_page_number())  # 下一页的页码
    print(page_two.has_previous())  # 是否有上一页
    print(page_two.previous_page_number())  # 上一页的页码

    # 抛出错误
    page = paginator.page(12)  # Error:EmptyPage
    page = paginator.page("z")  # Error:PageNotAnInteger
    """
    post_list = None
    if cid != -1:
        cat = BlogCategory.objects.get(id=cid)
        post_list = cat.post_set.all()
    elif tid != -1:
        tag = Tags.objects.get(id=tid)
        post_list = tag.post_set.all()
    else:
        post_list = Post.objects.all()

    #进行分页
    paginator = Paginator(post_list, 10)
    page = request.GET.get("page", 1)
    current_page = int(page)
    # post_list = paginator.page(current_page)  # 显示第1页的内容


    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)

    # 进行去重，过滤
    new_comment_list = Comment.objects.all()
    new_comment_list1 = []
    post_list1 = []
    for comment in new_comment_list:
        if comment.post.id not in post_list1:
            new_comment_list1.append(comment)
            post_list1.append(comment.post.id)

    ctx = {
        'post_list': post_list,
        'tags': tag_message_list,
        'new_comment_list': new_comment_list1,
        "page_range": paginator.page_range,
        "paginator": paginator,
        "current_page": current_page
    }
    return render(request, 'list.html', ctx)


def blog_detail(request,bid):
    post = Post.objects.get(id=bid)
    post.views = post.views + 1
    post.save()
    # 最新评论博客
    new_comment_list = Comment.objects.order_by('-pub_date').all()[:10]
    comment_list = post.comment_set.all()
    # 去重
    new_comment_list1 = []
    post_list1 = []
    for c in new_comment_list:
        if c.post.id not in post_list1:
            new_comment_list1.append(c)
            post_list1.append(c.post.id)

    # 博客标签
    tag_list = post.tags.all()
    # 相关推荐（标签相同的）
    post_recomment_list = set(Post.objects.filter(tags__in=tag_list)[:6])
    ctx = {
        'post': post,
        'new_comment_list': new_comment_list1,
        'post_recomment_list': post_recomment_list,
        'comment_list': comment_list

    }
    return render(request, 'show.html', ctx)

class CommentView(View):
    def get(self, request):
        pass
    def post(self, request, bid):

        comment = Comment()
        comment.user = request.user
        comment.post = Post.objects.get(id=bid)
        comment.content = request.POST.get('content')
        comment.pub_date = datetime.now()
        comment.save()
        # Ajax
        return HttpResponseRedirect(reverse("blog_detail", kwargs={"bid":bid}))