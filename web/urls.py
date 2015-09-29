# coding: utf-8

from django.conf.urls import include, url
from web import views

urlpatterns = [
    url(r'^$', "web.views.index"),
    url(r'^show_img/', 'web.views.show_img', name='show_img'),
]
