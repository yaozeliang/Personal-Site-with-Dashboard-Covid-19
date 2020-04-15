from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

# Django-taggit
from taggit.managers import TaggableManager
from django.utils import timezone
from PIL import Image
# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit





class Category(models.Model):
    
    name = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name




class ArticlePost(models.Model):
    author = models.ForeignKey(User, verbose_name='Author',on_delete=models.CASCADE)
    title = models.CharField('Title',max_length=100)
    body = models.TextField()
    created = models.DateTimeField('Created Time',default=timezone.now)
    updated = models.DateTimeField('Modified Time',auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='category'
    )

    tags = TaggableManager(blank=True)

    # avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    avatar = ProcessedImageField(
        upload_to='article/%Y%m%d',
        processors=[ResizeToFit(width=350)],
        format='JPEG',
        options={'quality': 100},
    )

    class Meta:
        verbose_name = 'Article'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self): 
        return reverse('article:article_detail', args=[str(self.id)])

    




    

    


