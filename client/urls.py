from django.urls import path
from . import views

urlpatterns = [
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    path('save_progres_changes/', views.save_progres_changes, name='save_progres_changes'),
    path('upload_profile_photo/', views.upload_profile_photo, name='upload_profile_photo'),
    path('contact/', views.contact_view, name='contact_view'),

    path('client', views.client, name="client"),
]
