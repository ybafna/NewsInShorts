from django.conf.urls import url,include
from getnews import views




urlpatterns = [

    #/news/
    url(r'^$',views.index, name="index"),
    url(r'^general/$', views.category, name="general"),
    url(r'^business/$', views.category, name="business"),
    url(r'^sport/$', views.category, name="sport"),
    url(r'^entertainment/$', views.category, name="entertainment"),
    url(r'^science_nature/$', views.category, name="science-nature"),
    url(r'^technology/$', views.category, name="technology"),
    url(r'^trending/$', views.trending, name="trending"),
    url(r'^(?P<paper_id>[0-9]+)/$',views.paper,name='paper'),
    url(r'^search/', views.search, name='search'),

]