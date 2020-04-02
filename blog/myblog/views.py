from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
import markdown
import re 
from .models import Category,Tag,Article
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
class IndexView(ListView):

	model = Article
	template_name = 'index.html'
	context_object_name = 'article_list'
	# 分页，每页10篇文章
	paginate_by = 10


class DetialView(DetailView):

	model = Article
	template_name = 'detial.html'
	context_object_name = 'article'

	def get(self,request,*args,**kwargs):
		# 重写get方法的目的是为了用户访问时阅读量加1
		# 先调用父类方法是为了获取self.object，即为被访问的文章对象
		response = super(DetialView,self).get(request,*args,**kwargs)
		article = self.object
		article.increase_views()
		# get方法必须返回httpResponse对象
		return response

	def get_object(self,queryset=None):
		# 重写该方法是为了对文章的body进行渲染
		article = super(DetialView,self).get_object(queryset=None)
		md = markdown.Markdown(extensions=[
								 'markdown.extensions.extra',
								 'markdown.extensions.codehilite',
								 'markdown.extensions.toc',])
		# 将body解析成html文本
		article.body = md.convert(article.body)
		m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
		if m.group(1) is not '':
			article.toc = md.toc
			print('-----%s'%m.group(1))
		else:
			article.toc = ''
		return article

	# # 查询id为pk的文章，如果找不到则返回404错误
	# article = get_object_or_404(Article,pk=pk)
	# # 用户访问文章详情页时，阅读量加1
	# article.increase_views()
	# md = markdown.Markdown(extensions=[
	# 							 'markdown.extensions.extra',
	# 							 'markdown.extensions.codehilite',
	# 							 'markdown.extensions.toc',])
	# # 将body解析成html文本
	# article.body = md.convert(article.body)
	# m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
	# if m.group(1) is not '':
	# 	article.toc = md.toc
	# 	print('-----%s'%m.group(1))
	# else:
	# 	article.toc = ''
		
	# return render(request,'detial.html',{'article':article})


# def  archive(request,year,month):
# 	article_list = Article.objects.filter(create_time__year=year
# 		                                  )

# 	return render(request,'index.html',context={'article_list':article_list})

class ArchiveView(IndexView):
	def get_queryset(self):
		return super(ArchiveView,self).get_queryset().filter(create_time__year=self.kwargs.get('year'))

class CategoryView(IndexView):
	# # article_list = Article.objects.filter(category__pk=pk)
	# cate = get_object_or_404(Category,pk=pk)
	# article_list = Article.objects.filter(category=cate).order_by('-create_time')

	# return render(request,'index.html',context={'article_list':article_list})
	# 默认会查找所有，所以重写该方法
	def get_queryset(self):
		# url的路径参数会保存在kwargs中，是一个字典，非路径参数保存在args中，是一个列表
		cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category=cate)


# def tag(request,pk):

# 	article_list = Article.objects.filter(tags__pk=pk).order_by('-create_time')
# 	return render(request,'index.html',context={'article_list':article_list})
class TagView(ListView):
	model = Article
	template_name = 'index.html'
	context_object_name = 'article_list'

	def get_queryset(self):

		return super(TagView,self).get_queryset().filter(tags__pk=self.kwargs.get('pk'))
	
