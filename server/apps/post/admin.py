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
admin.site.register(Feedback)
admin.site.register(Curation)
admin.site.register(CurationTable)
admin.site.register(BookMarkTable)
admin.site.register(LikeTable)
admin.site.register(Push)