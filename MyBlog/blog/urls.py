from django.urls import path,re_path
from . import views
#为了配置路径
from MyBlog.settings import MEDIA_ROOT
from django.views.static import serve

app_names = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    re_path('active/(?P<active_code>[a-zA-Z0-9]+)', views.ActiveView.as_view(), name='active'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('category/<int:cid>', views.blog_list, name='blog_list'),
    path('tags/<int:tid>/', views.blog_list, name='blog_list'),
    path('blog/<int:bid>/', views.blog_detail, name='blog_detail'),
    path('list/', views.blog_list, name='blog_list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('comment/<int:bid>/', views.CommentView.as_view(), name='comment'),
    #配置media的图片路径
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #path('media/(<str:path>.*)', serve, {"document_root": MEDIA_ROOT})
]
