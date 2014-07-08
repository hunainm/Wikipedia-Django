from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PagePrivacy(models.Model):
    Type = models.TextField()


class Page(models.Model):
    title = models.TextField(blank=False, null=False)
    content = models.TextField()
    modifyDate = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User)
    Privacy = models.ForeignKey(PagePrivacy)
    ModifyRequest = models.NullBooleanField()
    ModifiedContent = models.TextField()


class PageHistory(models.Model):
    Page = models.ForeignKey(Page)
    History = models.TextField()
    modifyDate = models.DateTimeField(auto_now=True)
    Modifier = models.ForeignKey(User)


class Notifications(models.Model):
    user = models.ForeignKey(User, null=False)
    message = models.TextField(blank=False)
    link = models.URLField()
    article=models.ForeignKey(Page)
    date = models.DateTimeField(auto_now=True)