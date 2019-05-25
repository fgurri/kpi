import nautilus.plots as p
import nautilus.queries as q
from django.shortcuts import render
import datetime
import dateutil.relativedelta


def dashboard(request):
    now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
    last_month = str(now.year) + str(now.month).zfill(2)
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
        'plot_distribution_new_patients': p.plot_distribution_new_patients(),
        'plot_distribution_new_patients_per_spec': p.plot_distribution_new_patients_per_spec(last_month, last_month)})


def plot_visits_per_month(request):
    return render(request, 'plot.html', {'plotdiv': p.plot_visits_per_month(),
                                        'footer': 'Número de visites al centre agrupat per mes.',
                                        'heading': 'Total visites > Evolució'})


def plot_visits_per_patient(request):
    footer = '<p>Distribució del número de visites per pacient.</p>'
    footer = footer + '<p>Per facilitar la visualització de les dades, els pacients amb més de 50 visites s\'han agrupat tots en el grup de 50 visites.</p>'
    return render(request, 'plot.html', {'plotdiv': p.plot_visits_per_patient(),
                                        'footer': footer,
                                        'heading': 'Fidelització > Distribució número de visites per pacient'})


def plot_casual_vs_fidelizied(request):
    plotdiv_patients, plotdiv_visits = p.plot_distribution_casual_vs_fidelizied()
    return render(request, 'casualvsFidelizied.html', {'plotdiv_patients': plotdiv_patients,
                                                        'plotdiv_visits': plotdiv_visits})



def plot_last_visits_per_month(request):
    footer = '<p>Número de últimes visites al centre agrupat per mes.</p>'
    footer = footer + '<p><ul>Mètode de càlcul:'
    footer = footer + '<li>Buscar la última visita de cada pacient</li>'
    footer = footer + '<li>Agrupar-les totes per mes i sumar-les</li></ul></p>'
    footer = footer + '<p>No compta el número de pacients que es perden perquè no tenim informació sobre si tornaran a visitar-se.</p>'
    footer = footer + '<p>Si tenim una estimació de la mitjana de mesos que triga un pacient en tornar a visitar-se podem fer un càlcul del volum de pacients actius. És a dir, si sabem que un pacient triga en promig 8 mesos en tornar a visitar-se al centre llavors sumant els valors dels últims 8 mesos tindrem el volum estimat de pacients actius amb els que treballa el centre</p>'

    return render(request, 'plot.html', {'plotdiv': p.plot_last_visits_per_month(),
                                        'footer': footer ,
                                        'heading': 'Fidelització > Fuga de pacients'})


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
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month
    return render(request, 'visitsSpeciality.html', {'plotdiv': p.plot_distribution_visits_per_speciality(monthini, monthfinal),
                                                            'monthini': monthini,
                                                            'monthfinal': monthfinal,
                                                            'listMonths': q.get_Months()})


def plot_new_patients_per_speciality(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month

    return render(request, 'newPatientsSpeciality.html', {'plotdiv': p.plot_distribution_new_patients_per_spec(monthini, monthfinal),
                                                            'monthini': monthini,
                                                            'monthfinal': monthfinal,
                                                            'listMonths': q.get_Months()})


def plot_new_patients_evolution_per_speciality(request):
    id_speciality = request.POST.get('id_speciality')
    if id_speciality is None:
        id_speciality = '19'

    return render(request, 'newPatientsEvolutionSpeciality.html', {'listSpecialities': q.get_Specialities(),
        'id_speciality': id_speciality,
        'plotdiv': p.plot_evolution_new_patients_per_spec(p_idEspeciality=id_speciality)})


def plot_new_patients_per_speciality_slider(request):
    rangevalue = request.POST.get('rangevalues')
    if rangevalue is None:
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        rangevalue = last_month + ", " + last_month

    monthini = rangevalue.replace("'", "").split(",")[0].strip()
    monthfinal = rangevalue.replace("'", "").split(",")[1].strip()
    sliderdict = "{value: [" + str(rangevalue.replace("'", "")) + "], "
    monthlist = q.get_month_list()
    sliderdict = sliderdict + "ticks: " + str(monthlist).replace("'", "") + ", "
    sliderdict = sliderdict + "ticks_positions: ["
    pos = 0
    tickpositiondelay = 100/(len(monthlist)-1)
    for i in range(len(monthlist)):
        sliderdict = sliderdict + str(pos)
        pos = pos + tickpositiondelay
        sliderdict = sliderdict + ","
    sliderdict = sliderdict + "],"
    sliderdict = sliderdict + "lock_to_ticks: true,  tooltip: 'show'}"
    return render(request, 'newPatientsSpeciality.html', {'plotdiv': p.plot_distribution_new_patients_per_spec(monthini, monthfinal),
                                                            'sliderdict': sliderdict})


def plot_new_patients_per_speciality_per_month(request):
    return render(request, 'newPatientsSpecialityMonth.html', {'plotdiv': p.plot_new_patients_per_speciality_per_month()})


def plot_first_blood_per_agenda(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')

    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month

    return render(request, 'firstBloodPerAgenda.html', {'plotdiv': p.plot_first_blood_per_agenda(monthini, monthfinal),
                                                            'monthini': monthini,
                                                            'monthfinal': monthfinal,
                                                            'listMonths': q.get_Months()})


def plot_first_blood_per_agenda_by_spec(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    id_speciality = request.POST.get('id_speciality')
    if id_speciality is None:
        id_speciality = '19'

    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month

    return render(request, 'firstBloodPerAgendaBySpec.html', {'plotdiv': p.plot_first_blood_per_agenda(monthini, monthfinal, p_idEspeciality=id_speciality),
                                                            'monthini': monthini,
                                                            'monthfinal': monthfinal,
                                                            'listMonths': q.get_Months(),
                                                            'listSpecialities': q.get_Specialities(),
                                                            'id_speciality': id_speciality})


def plot_month_frequency_by_agenda(request):
    id_agenda = request.POST.get('id_agenda')
    if id_agenda is None:
        id_agenda = 'AG100' #medicina general default

    return render(request, 'frequencyByAgenda.html', {'listAgendas': q.get_Agendas(),
                                                        'id_agenda': id_agenda,
                                                        'plotdiv': p.plot_frequency_per_agenda(id_agenda)})
