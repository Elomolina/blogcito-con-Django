from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
import os


class Tag(models.Model):
    caption = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.caption}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=600)
    image_name = models.ImageField(null=True, blank=True, upload_to="blog_images", default="blog_images/default_blog.png")
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="tags_post")
    def __str__(self):
        return f"{self.title}, created by {self.author}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= "user")
    biografia = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pictures", default="profile_pictures/default_profile.webp",blank=True, null=True)
    