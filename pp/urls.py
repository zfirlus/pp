from django.conf.urls import patterns, include, url
from main import views
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adminUsers/', views.adminUsers, name='adminUsers'),
    url(r'^adminCategories/', views.adminCategories, name='adminCategories'),
    url(r'^moderator/', views.moderator, name='moderator'),
    url(r'^categories/', views.categories, name='categories'),
    url(r'^(?P<cat_id>\d+)/projects/', views.projects, name='projects'),
    url(r'^projects/', views.projects, name='projects'),
)
