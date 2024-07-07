from django.contrib import admin
from .models import UserAccount, UserAccountManager, SearchLimit
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(SearchLimit)
