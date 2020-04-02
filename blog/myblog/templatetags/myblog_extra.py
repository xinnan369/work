from django import template
from ..models import Category,Tag,Article

register = template.Library()

@register.inclusion_tag('inclusions/_recent_article.html',takes_context=True)
def show_recent_article(context,num=3):
	return {'recent_article_list':Article.objects.all().order_by('-create_time')[:num]}

@register.inclusion_tag('inclusions/_archives.html',takes_context=True)
def show_archives(context):
	return {'date_list':Article.objects.dates('create_time','month','DESC')}

@register.inclusion_tag('inclusions/_category.html',takes_context=True)
def show_category(context):
	return {'category_list':Category.objects.all()}


@register.inclusion_tag('inclusions/_tags.html',takes_context=True)
def show_tags(context):
	return {'tag_list':Tag.objects.all()}