from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin
from wiki import views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'Page', views.PageViewSet)



urlpatterns = patterns('',
                       url(r'^/$','wiki.views.HomePage'),
                       url(r'^wiki/$', 'wiki.views.editor'),
                       url(r'^CreatePage/$', 'wiki.views.CreatePage'),
                       url(r'^EditPage/$', 'wiki.views.EditPage'),
                       url(r'^wikipedia/$', 'wiki.views.HomePage'),
                       url(r'^wikipedia/wiki/changes/(?P<page_name>\w+)$', 'wiki.views.ShowModifiedPage'),
                       url(r'^wikipedia/wiki/history/$', 'wiki.views.ShowHistoryPage'),
                       url(r'^wikipedia/wiki/(?P<page_name>\w+)$', 'wiki.views.ShowSearchPage'),
                       url(r'^delete/$', 'wiki.views.DeletePage'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^404/$', 'wiki.views.PageNotFound'),
                       url(r'^Edit/$', 'wiki.views.editPage'),
                       url(r'^acceptChanges/$', 'wiki.views.acceptChanges'),
                       url(r'^NewAccount/$', 'wiki.views.NewAccount'),
                       url(r'^CreateAccount/$', 'wiki.views.CreateAccount'),
                       url(r'^login/$', 'wiki.views.Login'),
                       url(r'^logout/$', 'wiki.views.Logout'),
                       url(r'^authenticate/$', 'wiki.views.authenticateUser'),
                       url(r'^history/$', 'wiki.views.ShowHistoryList'),
                       url(r'^SearchAcrossPages/$', 'wiki.views.SearchAcrossPages'),
                       url(r'^SearchAcrossTitles/$', 'wiki.views.SearchAcrossTitles'),
                       url(r'^Contributions/$', 'wiki.views.Contributions'),
                       url(r'^ViewAllNotifications/$', 'wiki.views.ViewAllNotifications'),
                       url(r'^', include(router.urls))




)
