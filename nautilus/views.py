from django.shortcuts import render, redirect
import datetime
import dateutil
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

import nautilus.plots as p
import nautilus.queries as q
import nautilus.utils as u
import kpi.settings as s
from nautilus.authentication import ActiveDirectoryBackend as adb


def login_form(request):
     # check if we have an autentification request
    username = request.POST.get('username')
    password = request.POST.get('password')
    messages = {}
    if username and password:
        user = adb.nautilus_authenticate(username, password)
        if user is not None:
            if s.NAUTILUS_REQUIRE_EXTERNAL_PERMISION:
                # we have a valid LDAP user, check if it allowed
                if q.is_user_allowed(username):
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('')
                else:
                    messages['message'] = "Login correcte però no té permisos per accedir a aquesta aplicació"
            else:
                # all authentified users are allowed
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('')
        else:
            messages['message'] = "Login incorrecte. Recordi que és el mateix usuari i contrasenya amb el que ha accedit a l'ordinador."
    return render(request, 'login.html', messages)


@login_required
def logout_form(request):
    # check if we have an autentification request
    if request.user is not None:
        logout(request)
    return redirect('login')


@login_required
def info(request):
    return render(request, 'panelInfo.html', {'load_array': q.get_last_loads(5),
                                            'agendas_list': q.get_Agendas()})


@login_required
def dashboard(request):
    now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
    last_month = str(now.year) + str(now.month).zfill(2)
    last_month_last_year = str(now.year-1) + str(now.month).zfill(2)
    return render(request, 'dashboard.html', {
        'v_last_month': u.yyyymmToMonthName(last_month),
        'v_previous_month': u.yyyymmToMonthName(u.yyyymm_add_months(last_month, -1)),
        'v_last_month_last_year': u.yyyymmToMonthName(last_month_last_year),
        'kpi_dict': q.get_KPI_general(6),
        'kpi_agendes': q.get_KPI_Agendas(last_month),
        'plot_rep_med_gen': p.plot_frequency_per_agenda('AG100'),
        'plot_rep_endos': p.plot_frequency_per_agenda('AG45'),
        'plot_patients': p.plot_patients_per_month(),
        'plot_new_patients': p.plot_new_patients_per_month(),
        'plot_distribution_new_patients': p.plot_distribution_new_patients(),
        'plot_distribution_new_patients_per_spec': p.plot_distribution_new_patients_per_spec(last_month, last_month)})


@login_required
def plot_visits_per_month(request):
    return render(request, 'plot.html', {'plotdiv': p.plot_visits_per_month(),
                                        'footer': 'Número de visites al centre agrupat per mes.',
                                        'heading': 'Total visites > Evolució'})


@login_required
def plot_visits_per_patient(request):
    footer = '<p>Distribució del número de visites per pacient.</p>'
    footer = footer + '<p>Per facilitar la visualització de les dades, els pacients amb més de 50 visites s\'han agrupat tots en el grup de 50 visites.</p>'
    return render(request, 'plot.html', {'plotdiv': p.plot_visits_per_patient(),
                                        'footer': footer,
                                        'heading': 'Fidelització > Distribució número de visites per pacient'})


@login_required
def plot_casual_vs_fidelizied(request):
    plotdiv_patients, plotdiv_visits = p.plot_distribution_casual_vs_fidelizied()
    return render(request, 'casualvsFidelizied.html', {'plotdiv_patients': plotdiv_patients,
                                                        'plotdiv_visits': plotdiv_visits})


@login_required
def plot_distance_to_lastmonth(request):
    footer = '<p></p>'
    return render(request, 'plot.html', {'plotdiv': p.plot_distance_to_lastmonth(),
                                        'footer': footer,
                                        'heading': 'Fidelització > Conteig mesos des de última visita'})


@login_required
def plot_last_visits_per_month(request):
    footer = '<p>Número de últimes visites al centre agrupat per mes.</p>'
    footer = footer + '<p><ul>Mètode de càlcul:'
    footer = footer + '<li>Buscar la última visita de cada pacient</li>'
    footer = footer + '<li>Agrupar-les totes per mes i sumar-les</li></ul></p>'
    footer = footer + '<p>No compta el número de pacients que es perden perquè no tenim informació sobre si tornaran a visitar-se.</p>'
    footer = footer + '<p>Si tenim una estimació de la mitjana de mesos que triga un pacient en tornar a visitar-se podem fer un càlcul del volum de pacients actius. És a dir, si sabem que un pacient triga en promig 8 mesos en tornar a visitar-se al centre llavors sumant els valors dels últims 8 mesos tindrem el volum estimat de pacients actius amb els que treballa el centre</p>'

    return render(request, 'plot.html', {'plotdiv': p.plot_last_visits_per_month(),
                                        'footer': footer ,
                                        'heading': 'Fidelització > Conteig últimes visites'})


@login_required
def plot_visits_per_month_speciality(request):
    id_speciality = request.POST.get('id_speciality')
    if id_speciality is None:
        id_speciality = '19'

    return render(request, 'visitsPerMonthSpeciality.html',
        {'listSpecialities': q.get_Specialities(),
        'id_speciality': id_speciality,
        'plotdiv': p.plot_visits_per_month_speciality(p_id_especiality=id_speciality)})


@login_required
def plot_visits_per_month_agenda(request):
    id_agenda = request.POST.get('id_agenda')
    if id_agenda is None:
        id_agenda = 'AG100' #medicina general default
    return render(request, 'visitsPerMonthAgenda.html',
        {'listAgendas': q.get_Agendas(),
        'id_agenda': id_agenda,
        'plotdiv': p.plot_visits_per_month_speciality(p_id_agenda=id_agenda)})


@login_required
def plot_visits_per_speciality(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month
    return render(request, 'visitsSpeciality.html', {'plotdiv': p.plot_distribution_visits_per_speciality(monthini, monthfinal),
                                                            'monthini': int(monthini),
                                                            'monthfinal': int(monthfinal),
                                                            'listMonths': q.get_Months()})


@login_required
def plot_new_patients_per_speciality(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    currYear = datetime.datetime.now().year

    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month

    return render(request, 'newPatientsSpeciality.html', {'plotdiv': p.plot_distribution_new_patients_per_spec(monthini, monthfinal),
                                                            'monthini': int(monthini),
                                                            'monthfinal': int(monthfinal),
                                                            'listMonths': q.get_Months(),
                                                            'listYears': q.get_Years(),
                                                            'currYear': str(currYear)})


@login_required
def plot_new_patients_evolution_per_speciality(request):
    id_speciality = request.POST.get('id_speciality')
    if id_speciality is None:
        id_speciality = '19'

    return render(request, 'newPatientsEvolutionSpeciality.html', {'listSpecialities': q.get_Specialities(),
        'id_speciality': id_speciality,
        'plotdiv': p.plot_evolution_new_patients_per_spec(p_id_especiality=id_speciality)})


@login_required
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


@login_required
def plot_new_patients_per_speciality_per_month(request):
    return render(request, 'newPatientsSpecialityMonth.html', {'plotdiv': p.plot_new_patients_per_speciality_per_month()})


@login_required
def plot_first_blood_per_agenda(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    currYear = datetime.datetime.now().year

    #check errors or missing values and set a default range
    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month

    return render(request, 'firstBloodPerAgenda.html', {'plotdiv': p.plot_first_blood_per_agenda(monthini, monthfinal),
                                                            'monthini': int(monthini),
                                                            'monthfinal': int(monthfinal),
                                                            'listMonths': q.get_Months(),
                                                            'listYears': q.get_Years(),
                                                            'currYear': str(currYear)})


@login_required
def plot_first_blood_per_agenda_by_spec(request):
    monthini = request.POST.get('monthini')
    monthfinal = request.POST.get('monthfinal')
    id_speciality = request.POST.get('id_speciality')
    if id_speciality is None:
        id_speciality = '19'

    currYear = datetime.datetime.now().year

    if monthini is None or monthini == '' or monthfinal is None or monthfinal == ''or int(monthini) > int(monthfinal):
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month).zfill(2)
        monthini = last_month
        monthfinal = last_month

    return render(request, 'firstBloodPerAgendaBySpec.html', {'plotdiv': p.plot_first_blood_per_agenda(monthini, monthfinal, p_id_especiality=id_speciality),
                                                            'monthini': int(monthini),
                                                            'monthfinal': int(monthfinal),
                                                            'listMonths': q.get_Months(),
                                                            'listSpecialities': q.get_Specialities(),
                                                            'id_speciality': id_speciality,
                                                            'listYears': q.get_Years(),
                                                            'currYear': str(currYear)})


@login_required
def plot_month_frequency_by_agenda(request):
    id_agenda = request.POST.get('id_agenda')
    if id_agenda is None:
        id_agenda = 'AG100' #medicina general default

    return render(request, 'frequencyByAgenda.html', {'listAgendas': q.get_Agendas(),
                                                        'id_agenda': id_agenda,
                                                        'plotdiv': p.plot_frequency_per_agenda(id_agenda)})

@login_required
def cc_period_performance(request):
    date_ini = request.POST.get('date_ini')
    date_fin = request.POST.get('date_fin')
    today = datetime.date.today()
    previous_month = today - relativedelta(months=1)
    start_previous_month = date(previous_month.year, previous_month.month, 1).strftime("%d/%m/%Y")
    end_previous_month = date(today.year, today.month, 1) - relativedelta(days=1)
    end_previous_month = end_previous_month.strftime("%d/%m/%Y")
    start_previous_week = today + datetime.timedelta(-today.weekday(), weeks=-1)
    start_previous_week = start_previous_week.strftime("%d/%m/%Y")
    end_previous_week = today + datetime.timedelta(-today.weekday() - 1)
    end_previous_week = end_previous_week.strftime("%d/%m/%Y")
    yesterday = today -relativedelta(days=1)
    today = today.strftime("%d/%m/%Y")
    yesterday = yesterday.strftime("%d/%m/%Y")

    if not date_ini or not date_fin:
        date_ini = today
        date_fin = today

    plot_distrib, plot_abs_values =  p.plots_callcenter_period(date_ini, date_fin)
    return render(request, 'callcenter_period_performance.html',{'plot_distrib': plot_distrib,
                                                            'plot_abs_values': plot_abs_values,
                                                            'date_ini': date_ini,
                                                            'date_fin': date_fin,
                                                            'today': today,
                                                            'yesterday': yesterday,
                                                            'start_previous_month': start_previous_month,
                                                            'end_previous_month': end_previous_month,
                                                            'start_previous_week': start_previous_week,
                                                            'end_previous_week': end_previous_week})
