from django.contrib import admin
from .models import Post, Path, Step, Category, Tag, TagTable
# Register your models here.


admin.site.register(Post)
admin.site.register(Path)
admin.site.register(Category)
admin.site.register(Step)
admin.site.register(Tag)
