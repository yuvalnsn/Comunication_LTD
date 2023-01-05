"""Comunication_LTD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
import config
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from interface.forms import CustomUserChangeForm
from django.conf.urls.static import static

urlpatterns = [
    path('interface/', include('interface.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(extra_context={'sec_lvl':config.sec_lvl},template_name="password_reset_sent.html")),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(extra_context={'sec_lvl':config.sec_lvl},template_name="password_reset_form.html",form_class = CustomUserChangeForm),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(extra_context={'sec_lvl':config.sec_lvl},template_name="password_reset_done.html"),name="password_reset_complete"),
    path('reset_password/', auth_views.PasswordResetView.as_view(extra_context={'sec_lvl': config.sec_lvl},template_name="password_reset.html"),name="reset_password"),

    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

