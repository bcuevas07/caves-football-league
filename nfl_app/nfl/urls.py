"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from nfl import views

urlpatterns = [
    url(r'home/$', views.home, name='home'),
    url(r'current_week/$', views.current_week, name='current_week'),
    url(r'weekly_schedule/$', views.weekly_schedule, name='weekly_schedule'),
    url(r'weekly_schedule/(?P<week>\d+)/$', views.ajax_week_schedule, name='get_week_schedule')
]