from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('pm', views.plot_visits_per_month, name='pm'),
    path('pepm', views.plot_visits_per_month_speciality, name='pepm'),
    path('papm', views.plot_visits_per_month_agenda, name='papm'),
    path('pcpe', views.plot_visits_per_speciality, name='pcpe')
]
