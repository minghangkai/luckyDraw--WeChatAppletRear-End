from django.contrib import admin

from .models import Topic
from .models import Article

admin.site.register(Topic)
admin.site.register(Article)
# Register your models here.
