"""sigcore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('account.urls')),
    path('', include('projet.urls')),
    path('email/', include(mail_urls)),

    path(
          'password-reset/',
          auth_views.PasswordResetView.as_view(
              template_name='account/reset/password_reset.html'
          ),
          name='password-reset'
      ),
    path(
          'password-reset/done/',
          auth_views.PasswordResetDoneView.as_view(
              template_name='account/reset/password_reset_done.html'
          ),
          name='password_reset_done'
      ),
    path(
          'password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
              template_name='account/reset/password_reset_confirm.html'
          ),
          name='password_reset_confirm'
      ),
    path(
          'password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(
              template_name='account/reset/password_reset_complete.html'
          ),
          name='password_reset_complete'
      ),
    #
    # path('Profile/password_change_done/', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='account/profile/password_change_done.html'),
    #     name='password_change_done'),
    # path('Profile/password_change/', auth_views.PasswordChangeView.as_view(
    #     template_name='account/profile/password_change.html'),
    #     name='password_change'),






] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
