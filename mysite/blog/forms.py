from django import forms
# 引入文章模型
from .models import Post

# 写文章的表单类
class PostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Post
        # 定义表单包含的字段
        fields = ('title', 'content','category','desc','tags')