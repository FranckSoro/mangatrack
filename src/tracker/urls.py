from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('library/', views.library, name='library'),
    path('library/add/', views.add_series, name='add_series'),
    path('library/<str:slug>/', views.series_detail, name='series_detail'),
    path('library/<str:slug>/edit/', views.edit_user_series, name='edit_user_series'),
    path('library/<str:slug>/edit-info/', views.edit_series, name='edit_series'),
    path('library/<str:slug>/delete/', views.delete_user_series, name='delete_series'),
    path('library/<str:slug>/add-chapter/', views.add_chapter, name='add_chapter'),
    path('library/<str:slug>/history/', views.reading_history, name='reading_history'),
    path('library/<str:slug>/history/<int:entry_id>/delete/', views.delete_reading_entry, name='delete_reading_entry'),
    path('history/', views.reading_history_global, name='reading_history_global'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
]

# URLs pour l'authentification (vues inline)
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html', next_page='tracker:login'), name='logout'),
    path('register/', views.register, name='register'),
]
