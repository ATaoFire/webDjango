from django.contrib import admin
from blog.models import Banner,Post,BlogCategory,Tags

admin.site.register(Banner)
admin.site.register(BlogCategory)
admin.site.register(Tags)
admin.site.register(Post)