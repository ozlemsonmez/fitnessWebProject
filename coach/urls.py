from django.urls import path
from . import views

urlpatterns = [
    path('save_coach_changes/', views.save_coach_changes, name='save_coach_changes'),
    path('upload_profile_photo/', views.upload_profile_photo, name='upload_profile_photo'),
    path('contact/', views.contact_view, name='contact_view'),
    path('edit_client/', views.edit_client, name='edit_client'),


    path('coach', views.coach, name="coach"),
]
