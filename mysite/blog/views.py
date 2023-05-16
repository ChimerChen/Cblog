from django.shortcuts import render,get_object_or_404
from django.db.models import Q,F
from .models import Category,Post,User
from comments.models import Comment
from django.core.paginator import Paginator
import markdown
from comments.forms import CommentForm
from .forms import PostForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by("-add_date")

     # 分页方法
    paginator = Paginator(post_list, 8)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj
    }
    return render(request, 'blog/index.html',context)

def category_list(request,category_id):
    category = get_object_or_404(Category,id=category_id)
   
    posts = category.post_set.all()
    # 分页方法
    paginator = Paginator(posts, 8)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj
    }
    return render(request,'blog/list.html',context)

def post_detail(request,post_id):
    post = get_object_or_404(Post,id=post_id)
     
     # 将markdown语法渲染成html样式
    post.content = markdown.markdown(post.content,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])
    comment_form = CommentForm()
    # 取出文章评论
    comments = Comment.objects.filter(article=post_id).order_by('-comment_time')
    # 用id实现上下篇
    prev_post = Post.objects.filter(id__lt = post_id).last()
    next_post = Post.objects.filter(id__gt = post_id).first()

    #用时间实现上下篇
    # prev_post = Post.objects.filter(add_date__lt = post.add_date).last()
    # next_post = Post.objects.filter(add_date__gt = post.add_date).first()
    
    
    Post.objects.filter(id = post_id).update(pv=F("pv")+1)


    context = { 'post':post,
               'prev_post':prev_post,
               'next_post':next_post,
               'comments':comments,
               'comment_form':comment_form}
    return render(request,'blog/detail.html',context)

def search(request):
    keyword = request.GET.get('keyword')
    tag = request.GET.get('tag')

    if not keyword:
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword)) 


    if tag and tag != 'None':
        post_list = post_list.filter(tags__name__in=[tag])
    # 分页方法
    paginator = Paginator(post_list, 8)  # 第二个参数代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'keyword':keyword,
        'tag':tag,
    }
    return render(request,'blog/index.html',context)

def archives(request,year,month):
    # 分页方法
    post_list = Post.objects.filter(add_date__year=year,add_date__month=month)
    

    # 第二个参数2代表每页显示几个
    paginator = Paginator(post_list,8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'post_list':post_list,
        'year':year,
        'month':month,
        'page_obj':page_obj
    }
    return render(request,'blog/archives_list.html',context)



#文章发布
@login_required(login_url='users:login') 
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = PostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            new_article.owner = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("blog:index")
        # 如果数据不合法，返回错误信息
        else:
            print(article_post_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = PostForm()
        category_list = Category.objects.all()
        # 赋值上下文
        context = { 'article_post_form': article_post_form,
                    'category_list' : category_list
                    }
        # 返回模板
        return render(request, 'blog/create.html', context)


   
