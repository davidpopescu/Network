from django.contrib import admin
from .models import Post
from .models import Profile
from .models import User
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile)
# Register your models here.
