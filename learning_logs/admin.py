from django.contrib import admin
from .models import Topic,Entry
# Register your models here.
admin.site.register(Entry)
admin.site.register(Topic)