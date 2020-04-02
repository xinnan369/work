from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


# Create your models here.
class Category(models.Model):
	'''文章分类模型类'''
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = '分类'
		verbose_name_plural = verbose_name


class Tag(models.Model):
	'''文章标签模型类'''
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name


class Article(models.Model):
	'''文章模型类'''

	# 文章标题,第一个位置参数为verbose_name
	title = models.CharField('标题',max_length=100)
	# 文章正文
	body = models.TextField('正文')
	# 创建时间
	create_time = models.DateTimeField('创建时间',default=timezone.now)
	# 修改时间
	modify_time = models.DateTimeField('修改时间')
	# 文章摘要，允许为空
	excerpt = models.CharField('摘要', max_length=300,blank=True)
	# 文章分类,一对多,因为外键的第一个参数必须为关联模型类，所以必须写上verbose_name
	category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
	# 文章标签,多对多,允许为空
	tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True)
	# 文章作者
	author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
	# 阅读量
	views = models.PositiveIntegerField('阅读量',default=0)

	def __str__(self):
		return self.title

	def save(self,*args,**kwargs):
		'''保存到数据库时调用'''
		self.modify_time = timezone.now()
		# 实例化markdown类，用于渲染html文本
		md = markdown.Markdown(extendions=
								['markdown.extendions.extra',
								 'markdown.extendions.codehilite',]
			)
		# 去掉html文本的html标签，并截取前54个字符赋给摘要
		self.excerpt = strip_tags(md.convert(self.body))[:54]
		super().save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('myblog:detial',kwargs={'pk':self.pk})

	def increase_views(self):
		self.views += 1
		# update_fiels告诉django只需要修改views字段即可，提高效率
		self.save(update_fields=['views'])

	class Meta:
		verbose_name = '文章'
		verbose_name_plural = verbose_name
		ordering = ['-create_time']