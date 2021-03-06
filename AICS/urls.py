"""AICS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from webmanager import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view),
    url(r'^register$', views.register_view, name='register'),
    url(r'^upload_cnn$', views.upload_cnn_view, name='upload_cnn'),
    url(r'^upload_svm$', views.upload_svm_view, name='upload_svm'),
    url(r'^select$', views.select_view, name='select'),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^index$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^success$', TemplateView.as_view(template_name="success.html"), name="success"),
    url(r'^app/$', views.app_view, name="app"),
]
