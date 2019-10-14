from django.urls import path
from . import views

app_names = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.blog_list, name='blog_list'),
    path('search$', views.SearchView.as_view(), name='search'),

]
