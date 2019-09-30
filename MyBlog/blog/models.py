from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self) \
            .get_queryset() \
            .filter(status='published')

class User(models.Model):
    #用户的性别
    STATUS_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    #unique=True是唯一值校验
    #用户名
    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    #用户密码
    userpassword = models.CharField(max_length=256, verbose_name="密码")
    #用户邮箱
    useremail = models.EmailField(unique=True, verbose_name="邮箱")
    #用户性别
    usersex = models.CharField(max_length=32, choices=STATUS_CHOICES, default='男', verbose_name="性别")
    #注册时间
    createdtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["createdtime"]
        verbose_name = '用户'
        verbose_name_plural = verbose_name


#邮箱验证
class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name='验证码', max_length=50,default='')
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name="验证码类型", choices=(("register",u"注册"),("forget","找回密码"), ("update_email","修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.datetime.now())

    class Meta:
        verbose_name = "邮箱验证码"
        # 复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

#轮播图
class Banner(models.Model):
    title = models.CharField('标题', max_length=50)
    #设置轮播图的路径
    cover = models.ImageField('轮播图', upload_to = 'banner/%Y/%m/%d/')
    link_url = models.URLField('图片链接', max_length=100)
    idx = models.IntegerField('索引')
    is_active = models.BooleanField('是否active', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

#博客分类模型
class BlogCategory(models.Model):
    name = models.CharField('分类名称', max_length=20, default='')
    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
#标签模型
class Tags(models.Model):
    name = models.CharField('标签名称', max_length=20, default='')
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#博客
class Post(models.Model):
    # 帖子状态选项，后面会用到
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '发布'),
    )

    # 作者，外键
    # 一个作者可以有多篇帖子
    # 当作者被删除，相应的帖子也会被删除
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts', to_field='username', verbose_name="作者")

    category = models.ForeignKey(BlogCategory, on_delete=models.SET_DEFAULT, verbose_name='博客分类', default=None)
    tags = models.ManyToManyField(Tags, verbose_name='标签')
    # 帖子标题，CharField数据库中会转换为VARCHAR
    title = models.CharField(max_length=250, verbose_name="标题")
    # 正文，TextField会转换为TEXT
    body = models.TextField(verbose_name="正文")
    # 发布日期，timezone.now：以时区格式返回当前的时间
    publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    #封面静态文件内容
    cover = models.ImageField('博客封面', upload_to='static/images/post', default=None)
    views = models.IntegerField('浏览数', default=0)
    recommend = models.BooleanField('推荐博客', default=False)

    # 简短的标记
    # slug指有效URL的一部分，能使URL更加清晰易懂。
    # 比如有这样一篇文章，标题是"13岁的孩子"，
    # 它的 URL 地址是"/posts/13-sui-de-hai-zi"，后面这一部分便是 slug。
    # 通过它构建有较好外观，SEO友好的URL
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish',   verbose_name="链接地址")

    # 创建时间，auto_now_add：当「创建」某个对象时，日期将被自动保存
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 最后一次更新时间，auto_now：当「保存」某对象时候，日期将被自动保存
    update = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 帖子的状态，choices选择STATUS_CHOICES元祖中的某一个状态
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', verbose_name="状态")

    class Meta:
        # 对publish字段进行排列，由「-」确定为降序
        ordering = ('-publish',)
        verbose_name = '提交'

        verbose_name_plural = verbose_name

    def __str__(self):
        # 增加人们可读对象表达方式
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

#评论区模型
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='博客')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='作者')
    pub_date = models.DateTimeField('发布时间')
    content = models.TextField('内容')

    def __str__(self):
        return self.content
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

#友情链接
class FriendlyLink(models.Model):
    title = models.CharField('标题', max_length=50)
    link = models.URLField('链接', max_length=50, default='')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
