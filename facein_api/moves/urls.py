from django.urls import path

from moves import views

app_name = 'moves'

urlpatterns = [
    path('move/', views.MoveView.as_view(), name='move'),
    path('cameras/', views.GetCameras.as_view(), name='company-cameras')
]
