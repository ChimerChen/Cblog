from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from blog.models import  Post
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Comment(MPTTModel):    #定义评论模型

    article = models.ForeignKey(Post,on_delete=models.DO_NOTHING,verbose_name='评论文章')
    comment_content = RichTextUploadingField(verbose_name="评论正文")
    comment_author = models.ForeignKey(to=User,on_delete=models.DO_NOTHING,verbose_name='评论者')
    comment_time = models.DateTimeField(verbose_name='评论时间',default=now)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)


    class MPTTMeta:
        order_insertion_by = ['comment_time']


    def __str__(self):
        return self.comment_content