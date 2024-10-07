from django.contrib import admin
from .models import *

#config to make admin prettier
class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date",)
    list_display = ("title", "date", "author","image_name")
    prepopulated_fields = {"slug": ("title",)}
# Register your models here.
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfileModel)