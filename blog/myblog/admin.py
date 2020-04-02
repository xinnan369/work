from django.contrib import admin
from myblog.models import Article,Category,Tag


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
	'''文章模型管理类'''

	list_display = ['title','create_time','modify_time','category','author']
	fields = ['title','body','excerpt','category','tags']

	def save_model(self,request,obj,form,change):
		obj.author = request.user
		
		super().save_model(request,obj,form,change)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)