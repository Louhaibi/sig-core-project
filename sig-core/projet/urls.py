from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, projet_list_view, AddProjet, UpdateProjet, DeleteProjet



app_name = 'projet'

urlpatterns = [

    path('home/', home, name='home'),
    path('projet/', projet_list_view.as_view(), name='list-projet'),
    path('createprojet/', AddProjet.as_view(), name='create-projet'),
    path('updateprojet/<int:pk>/', UpdateProjet.as_view(), name='update-projet'),
    path('deleteprojet/<int:pk>/', DeleteProjet.as_view(), name='delete-projet'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
