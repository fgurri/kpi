import nautilus.plots as p
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
        'plot_rep_med_gen': p.generate_prpa('AG100'),
        'plot_rep_endos': p.generate_prpa('AG45'),
        'plot_new_patients': p.generate_pnppm()})


def plotpm(request):
    return render(request, 'plot.html', {'plotdiv': p.generate_pm()})


def plotpepm(request):
    return render(request, 'plot.html', {'plotdiv': p.generate_pepm(13)})


def plotpcpe(request):
    return render(request, 'plot.html', {'plotdiv': p.generate_pcpe()})
