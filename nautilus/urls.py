from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('pm', views.plotpm, name='pm'),
    path('pepm', views.plotpepm, name='pepm'),
    path('pcpe', views.plotpcpe, name='pcpe')
]
