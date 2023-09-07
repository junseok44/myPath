from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64

User = get_user_model()

def get_user_by_username(username):
    try:
        print("find user")
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        print("create new user")
        newUser = User.objects.create_user(
            username=username, loginId="myOne", password='jang1234', intro='Test intro')
        return newUser

def get_image_from_dataUrl(dataUrl):
    image_data = None 
    if dataUrl:
        format, imgstr = dataUrl.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')

    return image_data
