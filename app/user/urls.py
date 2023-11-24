"""
URL mappings for the user API.
"""

from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'user'
router = DefaultRouter()
router.register(r'caregiver', views.CaregiverViewSet)
router.register(r'member', views.MemberViewSet)

router.register(r'job', views.JobViewSet)
router.register(r'job-application', views.JobApplicationViewSet)
router.register(r'appointment', views.AppointmentViewSet)
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('create', views.CreateUserView.as_view()),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls)),
]