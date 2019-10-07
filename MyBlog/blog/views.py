from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, User, Banner, BlogCategory, FriendlyLink, Tags
from .forms import UserForm, RegisterForm
import hashlib
#实现搜索
from django.views.generic.base import View
from django.db.models import Q

#分页机制
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
#增加加密算法
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def login(request):
    #设置不允许重复登陆
    if request.session.get('is_login', None):
        return redirect('/blog/home/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = '账号或密码不允许为空'
        if  login_form.is_valid():
            # 后面的username和password与login.html的元素名字保持一致
            username = request.POST.get("username", None)
            userpassword = request.POST.get("userpassword", None)
            if username and userpassword:  # 确保用户名和密码都不为空
                username = username.strip()
                try:
                    user = User.objects.get(username=username)
                    if user.userpassword == hash_code(userpassword) :
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_username'] = user.username
                        return redirect('/blog/home/')
                    else:
                        message = '账号或密码不正确，请重新输入'
                except:
                    message = '账号或密码不正确，请重新输入aa'
            return render(request, 'blog/login/login.html', locals())
    login_form=UserForm()
    return render(request, 'blog/login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/blog/home/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'blog/login/register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'blog/login/register.html', locals())
                same_email_user = User.objects.filter(useremail=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'blog/login/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = User.objects.create()
                new_user.username = username
                new_user.userpassword = hash_code(password1)
                new_user.useremail = email
                new_user.usersex = sex
                new_user.save()
                return redirect('/blog/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'blog/login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/blog/home/')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/blog/home/')
#首页
def home(request):
    banner_list = Banner.objects.all()
    recommend_list = Post.objects.filter(recommend=1)
    post_list = Post.objects.all().exclude(status__regex='draft')
    blogcategory_list = BlogCategory.objects.all()
    friendlylink_list = FriendlyLink.objects.all()
    contents = {
        'banner_list': banner_list,
        'recommend_list': recommend_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'friendlylink_list': friendlylink_list,
    }
    return render(request, 'blog/post/home.html', contents)

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

class SearchView(View):
    # def get(self, request):
    #     pass
    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw)|Q(content__icontains=kw))

        ctx = {
            'post_list': post_list
        }
        return render(request, 'blog/post/list.html', ctx)

#列表
def blog_list(request, cid = -1):
    post_list = None
    if cid != -1:
        cat = BlogCategory.objects.get(id=cid)
        post_list = cat.post_set.all()
    else:
        post_list = Post.objects.all()

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(post_list, per_page=1, request=request)

    post_list = p.page(page)

    tags = Tags.objects.all()
    tag_message_list = []
    # for t in tags:
    #     count = len(t.post_set.all())
    #     tm = TagMessage(t.id, t.name, count)
    #     tag_message_list.append(tm)

    ctx = {
        'post_list': post_list,
        'tags': tag_message_list
    }


    return render(request, 'blog/post/list.html', ctx)
