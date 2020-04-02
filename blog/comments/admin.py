from django.contrib import admin
from .models import Comments

# Register your models here.
class CommentsAdmin(admin.ModelAdmin):
	list_display = ['name','email','url','article','create_time']
	fields = ['name','email','url','text','article']

admin.site.register(Comments,CommentsAdmin)