from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^pokes$', views.pokes),
    url(r'^poke_action$', views.poke_action),
    url(r'^pokes/(?P<user_id>\d+)$', views.poke_action),
]