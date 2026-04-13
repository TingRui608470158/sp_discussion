from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pain-points/', views.PainPointListView.as_view(), name='painpoint_list'),
    path('pain-points/create/', views.PainPointCreateView.as_view(), name='painpoint_create'),
    path('pain-points/<int:pk>/', views.PainPointDetailView.as_view(), name='painpoint_detail'),
]
