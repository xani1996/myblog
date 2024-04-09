from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse
from extensions.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager


# Create your models here.

class HomeBanner(models.Model):
    hello = models.CharField(max_length=100)
    who_am_i = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='HomeBanner/', default='home-right.png')
    cv_button = models.CharField(max_length=50)
    cv_file = models.FileField(upload_to='cv/')
    contact_me_button = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'greeting'

    def __str__(self):
        return self.who_am_i


class AboutMe(models.Model):
    title = models.CharField(max_length=200)
    body = HTMLField()
    picture = models.ImageField(upload_to='AboutMe/')

    def __str__(self):
        return self.title


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model, HitCountMixin):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    body = HTMLField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishManager()
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    tags = TaggableManager()
    quotes = HTMLField(default='')
    image_one = models.ImageField(upload_to='post_image/', default='')
    image_two = models.ImageField(upload_to='post_image/', default='')

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=('-publish',))
        ]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def jpublish(self):
        return jalali_converter(self.publish)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, verbose_name=': نام شما')
    email = models.EmailField(verbose_name=': ایمیل')
    body = models.TextField(verbose_name=': متن مورد نظر')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, )

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
