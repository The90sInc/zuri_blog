from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  User
from django.urls import  reverse
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    update_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        #ordering = ['created', ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return  self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class PostComment(models.Model):
    post = models.ForeignKey(Post,
                                related_name='comments',
                                null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                                null=True, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'


    def __str__(self):
        return self.text