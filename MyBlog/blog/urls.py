from django.urls import path
from . import views

app_names = 'blog'
urlpatterns = [
    #主页
    path('home/', views.home, name='home'),
    #登录
    path('login/', views.login, name='login'),
    #注册
    path('register/', views.register, name='register'),
    #退出
    path('logout/', views.logout, name='logout'),
    path('list/', views.blog_list, name='blog_list'),
    path('category/(?P<cid>[0-9]+)/$', views.blog_list, name='blog_list'),

    path('search/', views.SearchView.as_view(), name='search'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail')
]
