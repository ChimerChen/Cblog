from django.contrib import admin
from .models import Post,Category,Sidebar
# Register your models here.
admin.site.register(Category)
admin.site.register(Sidebar)



class PostAdmin(admin.ModelAdmin):
    ''' 文章详情管理 '''

    list_display = ('id', 'title','category', 'tags', 'owner',  'pv', 'pub_date', )
    list_filter = ('owner',)
    search_fields = ('title', 'desc')
    list_display_links = ('id', 'title',)

admin.site.register(Post, PostAdmin)