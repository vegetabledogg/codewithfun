from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

def avatar_upload_path(instance, filename):
    return '/'.join(['avatar', str(instance.id)]) + '.jpg'

class User(AbstractUser):
    avatar = ProcessedImageField(upload_to=avatar_upload_path, default='avatar/default.jpg', verbose_name='头像', processors=[ResizeToFill(85,85)])

    def __str__(self):
        return self.username
