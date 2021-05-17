from django.urls import include
from django.urls import path
from rest_framework import routers

from profiles import views

router = routers.DefaultRouter()
router.register(r'staff', views.StaffViewSet, basename='staff')

app_name = 'profiles'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('check/<int:user_id>/room/<int:room_id>/', views.CheckAbilityToEnterRoomView.as_view(),
         name='check-room-access'),
]
