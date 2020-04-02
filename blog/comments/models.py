from django.db import models
from django.utils import timezone

# Create your models here.

class Comments(models.Model):

	name = models.CharField('名字',max_length=30)
	email = models.EmailField('邮箱')
	url = models.URLField('网址',blank=True)
	text = models.TextField('内容')
	create_time = models.DateTimeField('创建时间',default=timezone.now)
	article = models.ForeignKey('myblog.Article',verbose_name='文章',on_delete=models.CASCADE)

	class Meta:
		verbose_name = '评论'
		verbose_name_plural = verbose_name
		# 排序方式
		ordering = ['-create_time']

	def __str__(self):
		return '{}:{}'.format(self.name,self.text[:20])
