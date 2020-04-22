from django import template
from django.db.models.aggregates import Count
from ..models import ArticlePost,Category
 
register = template.Library()


@register.inclusion_tag('article/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': ArticlePost.objects.dates('created', 'month', order='DESC'),
    }


@register.inclusion_tag('article/inclusions/_cats_tags.html', takes_context=True)
def show_cats_tags(context):
    return {
        'tag_list': ArticlePost.tags.all(),
        'cat_list':Category.objects.all()
    }