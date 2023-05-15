from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property  # 缓存装饰器
from django.template.loader import render_to_string  # 渲染模板
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=10,verbose_name='分类名称')
    desc = models.TextField(max_length=200,blank=True,verbose_name='分类描述')
    add_date = models.DateField(default=now,verbose_name='添加时间')
    pub_date = models.DateField(auto_now=True,verbose_name='修改时间')
    # 文章标签
    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name




class Post(models.Model):
    title = models.CharField(max_length=60,verbose_name='文章标题')
    desc = models.TextField(max_length=200,blank=True,default='',verbose_name='文章描述')
    content =  RichTextUploadingField(verbose_name='文章详情')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类')
    add_date = models.DateField(default=now,verbose_name='添加时间')
    pub_date = models.DateField(auto_now=True,verbose_name='修改时间')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    pv = models.IntegerField(default=0,verbose_name="浏览量")
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title
    
     # 获取文章地址
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
    
class Sidebar(models.Model):

    STATUS = (
        (1, '隐藏'),
        (2, '展示')
    )

    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '最新文章'),
        (3, '最热文章'),
        (4, '最近评论'),
        (5, '文章归档'),
        (6, 'HTML')
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, default='', verbose_name="内容",
                               help_text="如果设置的不是HTML类型，可为空")
    sort = models.PositiveIntegerField(default=1,  verbose_name="排序", help_text='序号越大越靠前')
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="状态")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "侧边栏"
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title
    
    @classmethod #类方法装饰器，可以调用该方法
    def get_sidebar(cls):
        return cls.objects.filter(status=2)
    
    @classmethod #类方法装饰器，可以调用该方法
    def get_sidebar_search(cls):
        return cls.objects.get(display_type=1)
    
    @classmethod #类方法装饰器，可以调用该方法
    def get_sidebar_archive(cls):
        return cls.objects.get(display_type=5)
    
    #get方法返回一个对象，filter返回一个对象数组


    @property
    def get_content(self):
       
        if self.display_type == 1:
            context = {

            }
            return render_to_string('blog/sidebar/search.html',context=context)
        
        elif self.display_type == 2:
            context = {

            }
            return render_to_string('blog/sidebar/new_post.html',context=context)
        
        elif self.display_type == 3:
            context = {

            }
            return render_to_string('blog/sidebar/hot_post.html',context=context)
        
        elif self.display_type == 4:
            context = {

            }
            return render_to_string('blog/sidebar/comment.html',context=context)
        
        elif self.display_type == 5:
            context = {

            }
            return render_to_string('blog/sidebar/archives.html',context=context)
        
        elif self.display_type == 6:

            return self.content #在侧边栏直接使用这里的html，模板中必须使用safe过滤器去渲染html