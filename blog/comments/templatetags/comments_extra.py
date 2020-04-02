from django import template
from ..forms import CommentsForms

register = template.Library()

@register.inclusion_tag('inclusions/_forms.html',takes_context=True)
def show_comment_form(context,article,form=None):
	if form is  None:
		form = CommentsForms()
	return {'article':article,'form':form}

@register.inclusion_tag('inclusions/_list.html',takes_context=True)
def show_comment(context,article):
	# 获取该文章的所有评论
	comment_list = article.comments_set.all().order_by('-create_time')
	comment_count = comment_list.count()
	return {'comment_list':comment_list,
			'comment_count':comment_count}