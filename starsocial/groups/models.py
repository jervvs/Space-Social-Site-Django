from django.db import models
from django.utils.text import slugify #text formatting library
import misaka #markdown inside posts
from django.urls import reverse

from django.contrib.auth import get_user_model #get user model that's active in this project
User = get_user_model() #current user session

from django import template
register = template.Library() #custom template tagging

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug=models.SlugField(allow_unicode=True, unique=True)
    description =models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
