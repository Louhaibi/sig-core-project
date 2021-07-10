from django.urls import path, include
from .views import loginpage, Profile, registerpage, logoutUser, about, contact, VerificationView, change_password
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


app_name = 'account'

urlpatterns = [

    path('', loginpage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerpage, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('Profile/', Profile, name="Profile-page"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),
    path('Profile/password_change/', change_password, name='password_change')


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
