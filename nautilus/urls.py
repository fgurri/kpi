from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name=''),
    path('dashboard', views.dashboard, name='dashboard'),
    path('pm', views.plot_visits_per_month, name='pm'),
    path('pepm', views.plot_visits_per_month_speciality, name='pepm'),
    path('papm', views.plot_visits_per_month_agenda, name='papm'),
    path('pcpe', views.plot_visits_per_speciality, name='pcpe'),
    path('nppe', views.plot_new_patients_per_speciality, name='nppe'),
    path('nptpe', views.plot_new_patients_evolution_per_speciality, name='nptpe'),
    path('nppepm', views.plot_new_patients_per_speciality_per_month, name='nppepm'),
    path('fbpa', views.plot_first_blood_per_agenda, name='fbpa'),
    path('fbpaps', views.plot_first_blood_per_agenda_by_spec, name='fbpaps'),
    path('fpa', views.plot_month_frequency_by_agenda, name='fpa')
]
