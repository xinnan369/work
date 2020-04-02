from django.shortcuts import render,get_object_or_404,redirect
from .forms import CommentsForms
from myblog.models import Article
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages
# Create your views here.
@require_POST
def comment(request,pk):
	article = get_object_or_404(Article,pk=pk)
	# 用户的数据保存在post中，创建一个绑定了用户数据的表单实例
	form = CommentsForms(request.POST)
	# 验证表单数据的合法性
	if form.is_valid():
		# 调用表单实例的save方法可以创建comment模型类实例
		# commit=False的作用是仅仅利用表单中的数据生成模型类实例，但是并不保存进数据库
		comment = form.save(commit=False)
		# 将文章和评论关联起来，然后保存进数据库
		comment.article = article
		comment.save()
		messages.add_message(request,messages.SUCCESS,'评论发表成功',extra_tags='success')
		# 用户提交评论后，跳转到文章详情页
		# redirect参数也可以时定义了get_absolute_url方法的模型类
		return redirect(reverse('myblog:detial',kwargs={'pk':pk}))
	# 若数据不合法，则渲染一个页面，展示表单的错误
	context = {'article':article,'form':form}
	messages.add_message(request,messages.ERROR,'评论发表失败，请重新编辑后发送',extra_tags='danger')
	return render(request,'preview.html',context)