from django.urls import path
from . import views

app_name = 'myblog'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('article/<int:pk>',views.DetialView.as_view(),name='detial'),
    path('archive/<int:year>/<int:month>',views.ArchiveView.as_view(),name='archive'),
    path('category/<int:pk>',views.CategoryView.as_view(),name='category'),
    path('tag/<int:pk>',views.TagView.as_view(),name='tag'),

]
