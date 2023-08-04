from django.contrib import admin
from .models import User
from .models import Post, Path, Step
# Register your models here.


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Path)

admin.site.register(Step)
