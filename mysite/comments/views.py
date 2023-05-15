from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from blog.models import Post
from .forms import CommentForm
from .models import Comment

# 文章评论
@login_required(login_url='/user/login/')
def post_comment(request, article_id):
    article = get_object_or_404(Post, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.comment_author = request.user
            new_comment.save()
            return redirect(article)
        else:
            print(comment_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")
    
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")
