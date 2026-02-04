from django.urls import path
from .views import LandingView, submit_lead, save_test_result

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('api/lead/', submit_lead, name='submit_lead'),
    path('api/save-test-result/', save_test_result, name='save_test_result'),
]
