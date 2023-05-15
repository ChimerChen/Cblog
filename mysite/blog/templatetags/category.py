from django import template
from blog.models import  Category,Post,Sidebar

register = template.Library()


@register.simple_tag
def get_category_list():
    return Category.objects.all()

@register.simple_tag
def get_new_post():
    return Post.objects.order_by('-pub_date')[:8]

@register.simple_tag
def get_sidebar_list():
    return Sidebar.get_sidebar()

@register.simple_tag
def get_sidebar_search():
    return Sidebar.get_sidebar_search()

@register.simple_tag
def get_sidebar_archive():
    return Sidebar.get_sidebar_archive()


@register.simple_tag
def get_hot_post():
    return Post.objects.order_by('-pv')[:8]

@register.simple_tag
def get_archives():
    return Post.objects.dates('add_date','month',order='DESC')[:8]


