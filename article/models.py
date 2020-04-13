from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


from django.utils import timezone

# Create your models here.

# 博客文章数据模型
class ArticlePost(models.Model):
    author = models.ForeignKey(User, verbose_name='Author',on_delete=models.CASCADE)
    title = models.CharField('Title',max_length=100)
    body = models.TextField()
    created = models.DateTimeField('Created Time',default=timezone.now)
    updated = models.DateTimeField('Modified Time',auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Article'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    # def get_absolute_url(self): # new
    #     return reverse('article_detail', args=[str(self.id)])