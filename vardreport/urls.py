from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/logout/', views.admin_logout_redirect, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', views.user_dashboard, name='user_dashboard'),
    path('select-constituency/', views.select_constituency, name='select_constituency'),
    path('ajax/load-local-bodies/', views.load_local_bodies, name='load_local_bodies'),
    path('ajax/load-wards/', views.load_wards, name='load_wards'),
    path('form/', views.meeting_form, name='meeting_form'),
    path('meeting-success/', views.meeting_success, name='meeting_success'),
    path('submission-history/', views.submission_history, name='submission_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
