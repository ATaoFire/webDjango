from django.urls import path
from . import views

app_names = 'blog'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail')
]
