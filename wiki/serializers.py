from rest_framework import serializers
from wiki.models import Page

class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ('title', 'content', 'modifyDate')
