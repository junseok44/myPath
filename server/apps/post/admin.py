from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Curation)
admin.site.register(CurationTable)
admin.site.register(BookMarkTable)
admin.site.register(LikeTable)