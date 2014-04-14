from django.conf.urls import patterns, include, url
from main import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adminUsers/', views.adminUsers, name='adminUsers'),
    url(r'^adminCategories/', views.adminCategories, name='adminCategories'),
    url(r'^moderator/', views.moderator, name='moderator'),
    url(r'^categories/', views.categories, name='categories'),
    url(r'^(?P<cat_id>\d+)/projects/', views.projects, name='projects'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^project/(?P<pro_id>\d+)/', views.project, name='project'),
    url(r'^rejestracja/$',views.UserRegister, name='register'),
    url(r'^nowyprojekt/$',views.AddNewProject, name='newproject'),
    url(r'^edytujprojekt/(?P<project_id>\d+)/$',views.EditProject, name='editproject'),
    url(r'^logowanie/$', views.Signin, name='signin'),
)
