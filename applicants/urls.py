from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Profile
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    
    # Application
    path('applications/', views.application_list_view, name='application_list'),
    path('applications/create/', views.application_create_view, name='application_create'),
    path('applications/<int:pk>/', views.application_detail_view, name='application_detail'),
    path('dormitory/', views.dormitory_request_view, name='dormitory_request'),

    # Career Test
    path('career-test/', views.career_test_view, name='career_test'),
    
    # Documents
    path('documents/', views.document_list_view, name='document_list'),
    path('documents/upload/', views.document_upload_view, name='document_upload'),
]
