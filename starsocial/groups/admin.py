from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Group)

#tabular inline for child models
class GroupMemberInline(admin.TabularInline):
    model=models.GroupMember
