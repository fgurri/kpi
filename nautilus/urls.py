from django.urls import path
from . import views
import django.views.static
#import kpi.settings as s

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
    path('fpa', views.plot_month_frequency_by_agenda, name='fpa'),
    path('lvpm', views.plot_last_visits_per_month, name='lvpm'),
    path('vpp', views.plot_visits_per_patient, name='vpp'),
    path('pcpf', views.plot_casual_vs_fidelizied, name='pcpf'),
    path('dtlv', views.plot_distance_to_lastmonth, name='dtlv'),
    path('info', views.info, name='info'),
    path('login', views.login_form, name='login'),
    path('logout', views.logout_form, name='logout'),
    path('ccpf', views.cc_period_performance, name='ccpf'),
    path('ccevo', views.cc_evolution, name='ccevo'),
    path('ccrpe', views.cc_ext_performance, name='ccrpe'),
]
