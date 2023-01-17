from django.contrib import admin
from .models import Todo, Account, Schedule

# Register your models here.
admin.site.register(Todo)
admin.site.register(Account)
admin.site.register(Schedule)
