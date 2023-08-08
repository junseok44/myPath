from django.contrib import admin
from apps.post.models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Path)
admin.site.register(Step)
admin.site.register(Category)
admin.site.register(CategoryTable)
admin.site.register(Tag)
admin.site.register(TagTable)