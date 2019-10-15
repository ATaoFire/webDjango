from django.contrib import admin
from blog.models import Banner,Post,BlogCategory,Tags,FriendlyLink

admin.site.register(Banner)
admin.site.register(BlogCategory)
admin.site.register(Tags)
admin.site.register(FriendlyLink)
# admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js=(
            'js/editor/kindeditor-all.js',
            'js/editor/config.js',
        )
admin.site.register(Post,PostAdmin)