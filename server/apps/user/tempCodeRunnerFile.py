from apps.user.models import User
from apps.post.models import Post, BookMarkTable, LikeTable
# Create your views here.
user = User.objects.get(id=pk)
print(user.id)