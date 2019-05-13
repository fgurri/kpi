import nautilus.plots as p
import nautilus.queries as q
from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard.html', {'v_visits_total' : 1580502,
        'v_visits_current_year': 73642,
        'v_visits_last_year': 67059,
        'v_patients_total': 100879,
        'v_patients_current_year': 18757,
        'v_patients_last_year': 17396,
        'v_new_patients_current_year': 2227,
        'v_new_patients_last_year': 2360,
        'v_fidelity_total': 15.67,
        'v_fidelity_current_year': 3.93,
        'v_fidelity_last_year': 3.85,
        'plot_rep_med_gen': p.plot_frequency_per_agenda('AG100'),
        'plot_rep_endos': p.plot_frequency_per_agenda('AG45'),
        'plot_patients': p.plot_patients_per_month(),
        'plot_new_patients': p.plot_new_patients_per_month(),
        'plot_distribution_new_patients': p.plot_distribution_new_patients()})


def plot_visits_per_month(request):
    return render(request, 'plot.html', {'plotdiv': p.plot_visits_per_month()})


def plot_visits_per_month_speciality(request):
    id_speciality = request.POST.get('id_speciality')
    if id_speciality is None:
        id_speciality = '19'

    return render(request, 'visitsPerMonthSpeciality.html',
        {'listSpecialities': q.get_Specialities(),
        'id_speciality': id_speciality,
        'plotdiv': p.plot_visits_per_month_speciality(p_idEspeciality=id_speciality)})


def plot_visits_per_month_agenda(request):
    id_agenda = request.POST.get('id_agenda')
    if id_agenda is None:
        id_agenda = 'AG100' #medicina general default
    return render(request, 'visitsPerMonthAgenda.html',
        {'listAgendas': q.get_Agendas(),
        'id_agenda': id_agenda,
        'plotdiv': p.plot_visits_per_month_speciality(p_idAgenda=id_agenda)})

def plot_visits_per_speciality(request):
    return render(request, 'plot.html', {'plotdiv': p.plot_visits_per_speciality()})
