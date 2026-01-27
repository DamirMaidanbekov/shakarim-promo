from django.urls import path
from .views import LandingView, submit_lead

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('api/lead/', submit_lead, name='submit_lead'),
]
