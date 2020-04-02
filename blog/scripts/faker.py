import os
import sys
import pathlib
import random
from datetime import timedelta
import django
import faker
from django.utils import timezone

# 将项目根目录添加到python搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
	
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog.settings')
	django.setup()

	from myblog.models import Article,Tag,Category
	from comments.models import Comments
	from django.contrib.auth.models import User

	print('clean database')
	Article.objects.all().delete()
	Tag.objects.all().delete()
	Category.objects.all().delete()
	Comments.objects.all().delete()
	User.objects.all().delete()

	print('create a blog user')
	user = User.objects.create_superuser('admin', 'admin@hellogithub.com', 'admin')

	category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
	tag_list = ['django', 'Python', 'Pipenv', 'Docker', 'Nginx', 'Elasticsearch', 'Gunicorn', 'Supervisor', 'test tag']
	a_year_ago = timezone.now() - timedelta(days=365)

	print('create categories and tags')
	for cate in category_list:
	    Category.objects.create(name=cate)

	for tag in tag_list:
	    Tag.objects.create(name=tag)
 
	print('create a markdown sample article')
	Article.objects.create(
	    title='Markdown 与代码高亮测试',
	    body=pathlib.Path(BASE_DIR).joinpath('scripts', 'md.sample').read_text(encoding='utf-8'),
	    category=Category.objects.create(name='Markdown测试'),
	    author=user,
	)

	print('create some faked articles published within the past year')
	fake = faker.Faker()  # English
	for _ in range(100):
	    tags = Tag.objects.order_by('?')
	    tag1 = tags.first()
	    tag2 = tags.last()
	    cate = Category.objects.order_by('?').first()
	    create_time = fake.date_time_between(start_date='-1y', end_date="now",
	                                          tzinfo=timezone.get_current_timezone())
	    article = Article.objects.create(
	        title=fake.sentence().rstrip('.'),
	        body='\n\n'.join(fake.paragraphs(10)),
	        create_time=create_time,
	        category=cate,
	        author=user,
	    )
	    article.tags.add(tag1, tag2)
	    article.save()

	fake = faker.Faker('zh_CN')
	for _ in range(100):  # Chinese
	    tags = Tag.objects.order_by('?')
	    tag1 = tags.first()
	    tag2 = tags.last()
	    cate = Category.objects.order_by('?').first()
	    create_time = fake.date_time_between(start_date='-1y', end_date="now",
	                                          tzinfo=timezone.get_current_timezone())
	    article = Article.objects.create(
	        title=fake.sentence().rstrip('.'),
	        body='\n\n'.join(fake.paragraphs(10)),
	        create_time=create_time,
	        category=cate,
	        author=user,
	    )
	    article.tags.add(tag1, tag2)
	    article.save()

	print('create some comments')
	for article in Article.objects.all()[:20]:
	    article_create_time = article.create_time
	    delta_in_days = '-' + str((timezone.now() - article_create_time).days) + 'd'
	    for _ in range(random.randrange(3, 15)):
	        Comments.objects.create(
	            name=fake.name(),
	            email=fake.email(),
	            url=fake.uri(),
	            text=fake.paragraph(),
	            create_time=fake.date_time_between(
	                 start_date=delta_in_days, 
	                 end_date="now", 
	                 tzinfo=timezone.get_current_timezone()),
	            article=article,
	        )

	print('done!')