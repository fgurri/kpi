from django.db import connections
import configparser
import datetime

import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly as py
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import dateutil.relativedelta

import nautilus.utils as u
import nautilus.queries as q

""" Generates a offline plotly plot with the graph 'total visits per month'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_visits_per_month()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param:
    :rtype: string
"""
def plot_visits_per_month():
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_month as Mes, CONCAT(f_year, "-", f_monthname) as MesNom, sum(f_count) as Total FROM datawarehouse.dm1_visits_per_agenda GROUP BY f_month,  CONCAT(f_year, "-", f_monthname) ORDER BY f_month ASC'

        df = pd.read_sql(sql, connection)
        trace_visites = go.Scatter(x=df['MesNom'],
                            y=df['Total'],
                            mode='lines+markers',
                            name='Visites per mes')

        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['Total'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression_visites = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='Tendencia')

        trace_omi_annotation = go.Scatter(x=["2017-Dec", "2017-Dec"],
                            y=[0, df['Total'].max()],
                            mode='lines',
                            name='Inici odontologia a OMI360',
                            line=dict(dash='dot'))

        data = [trace_visites, trace_regression_visites, trace_omi_annotation]
        layout = go.Layout(
            title='Evolució del número de visites per mes',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'),
            yaxis=dict(titlefont=dict(family='Arial, sans-serif',
                                      size=18,
                                      color='lightgrey'),
                       showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Distribution of visits per speciality'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_distribution_visits_per_speciality('201801', '201812')
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param p_first_month: starting month of range values in YYYYMM format
    :param p_last_month: ending month of range values in YYYYMM format
    :rtype: string
"""
def plot_distribution_visits_per_speciality(p_first_month, p_last_month):
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_nomEspecialitat as Spec, sum(f_count) as Total FROM datawarehouse.dm1_visits_per_agenda WHERE f_month >= '+str(p_first_month)+' and f_month <= '+str(p_last_month)+' GROUP BY f_nomEspecialitat ORDER BY sum(f_count) DESC'
        df = pd.read_sql(sql, connection)

        trace = go.Pie(labels=df['Spec'], values=df['Total'])

        graph_title = 'Distribució visites per especialitat (Del ' + u.yyyymmToMonthName(p_first_month) + ' al ' + u.yyyymmToMonthName(p_last_month) + ')'
        data = [trace]
        layout = go.Layout(
              title=graph_title,
              titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
              autosize=False,
              width=1000,
              height=700,
              xaxis=dict(showticklabels=True,
                         tickangle=45,
                         tickfont=dict(family='Old Standard TT, serif',
                                       size=14,
                                       color='black'),
                         showexponent='none'),
              yaxis=dict(titlefont=dict(family='Arial, sans-serif',
                                        size=18,
                                        color='lightgrey'),
                         showticklabels=True,
                         tickfont=dict(family='Old Standard TT, serif',
                                       size=14,
                                       color='black'),
                         showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Visits per month by speciality'.
    You can choose to filter by speciality or by agenda, but one of both must be set.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_visits_per_month_speciality(p_id_especiality=19)
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param p_id_especiality: speciality identifier
    :param p_id_agenda: agenda identifier
    :rtype: string
"""
def plot_visits_per_month_speciality(p_id_especiality=None, p_id_agenda=None):
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT CONCAT(f_year, "-", f_monthname) as MesNom, f_month, sum(f_count) as Total FROM datawarehouse.dm1_visits_per_agenda WHERE '
        if (p_id_especiality is None) and (p_id_agenda is None):
            p_id_especiality = 19 # medicina general per defecte
        if (p_id_especiality is not None) and (p_id_especiality != ""):
            sql = sql + 'f_idEspecialitat='+str(p_id_especiality)+' '
        else:
            if (p_id_agenda is not None) and (p_id_agenda != ""):
                sql = sql + 'f_idAgenda=\''+str(p_id_agenda)+'\' '
        sql = sql + 'GROUP BY CONCAT(f_year, "-", f_monthname), f_month ORDER BY f_month ASC'

        df = pd.read_sql(sql, connection)
        if df.empty:
            return None
        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['Total'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='Tendencia Especialitat')

        trace = go.Scatter(x=df['MesNom'],
                            y=df['Total'],
                            mode='lines+markers',
                            name='Visites per mes')

        graph_title = 'Evolució mensual de visites'
        if p_id_especiality is not None:
            graph_title = q.get_Spec_Name(p_id_especiality) + ': '+ graph_title
        if p_id_agenda is not None:
            graph_title = q.get_Agenda_Name(p_id_agenda) + ': '+ graph_title
        data = [trace, trace_regression]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'),
            yaxis=dict(titlefont=dict(family='Arial, sans-serif',
                                      size=18,
                                      color='lightgrey'),
                       showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Frequency by agenda'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_frequency_per_agenda(p_id_agenda='AG100')
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param p_id_agenda: agenda identifier
    :rtype: string
"""
def plot_frequency_per_agenda(p_id_agenda):
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT CONCAT(f_year, "-", f_monthname) as MesNom, f_month as Mes, f_count/f_patients as rep FROM datawarehouse.dm1_visits_per_agenda WHERE f_idAgenda=\''+str(p_id_agenda)+'\' ORDER BY f_month ASC'

        df = pd.read_sql(sql, connection)
        trace_frequency = go.Scatter(x=df['MesNom'],
                            y=df['rep'],
                            mode='lines+markers',
                            name='repetitivitat')

        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['rep'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='regressio repetitivitat')

        graph_title = q.get_Agenda_Name(p_id_agenda) + ': repetitivitat'
        data = [trace_frequency, trace_regression]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'),
            yaxis=dict(showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Patients per month'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_patients_per_month()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_patients_per_month():
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_month as Mes , CONCAT(LEFT(f_month, 4), "-", f_monthname) as MesNom, f_patients as Patients, f_new_patients FROM datawarehouse.dm2_stats_per_month ORDER BY f_month ASC'

        df = pd.read_sql(sql, connection)
        trace_patients = go.Scatter(x=df['MesNom'],
                            y=df['Patients'],
                            mode='lines+markers',
                            name='Total pacients')

        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['Patients'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression_patients = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='Tendencia total pacients')

        trace_omi_annotation = go.Scatter(x=["2017-Dec", "2017-Dec"],
                            y=[0, df['Patients'].max()],
                            mode='lines',
                            name='Inici odontologia a OMI360',
                            line=dict(dash='dot'))

        graph_title = 'Pacients per mes'
        data = [trace_patients, trace_regression_patients, trace_omi_annotation]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'),
            yaxis=dict(showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'New patients per month'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_new_patients_per_month()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_new_patients_per_month():
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_month as Mes, CONCAT(LEFT(f_month, 4), "-", f_monthname) as MesNom, f_patients as Patients, f_new_patients as NewPatients FROM datawarehouse.dm2_stats_per_month ORDER BY f_month ASC'

        df = pd.read_sql(sql, connection)
        trace_new_patients = go.Scatter(x=df['MesNom'],
                            y=df['NewPatients'],
                            mode='lines+markers',
                            name='Pacients nous')

        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['NewPatients'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression_new_patients = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='Tendencia nous pacients')

        trace_omi_annotation = go.Scatter(x=["2017-Dec", "2017-Dec"],
                            y=[0, df['NewPatients'].max()],
                            mode='lines',
                            name='Inici odontologia a OMI360',
                            line=dict(dash='dot'))

        graph_title = 'Pacients nous per mes'
        data = [trace_new_patients, trace_regression_new_patients, trace_omi_annotation]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'),
            yaxis=dict(showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Distribution patients vs new patients'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_distribution_new_patients()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_distribution_new_patients():
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_month as Mes, CONCAT(LEFT(f_month, 4), "-", f_monthname) as MesNom, f_patients-f_new_patients as Patients, f_new_patients as NewPatients FROM datawarehouse.dm2_stats_per_month ORDER BY f_month ASC'
        df = pd.read_sql(sql, connection)

        trace_new_patients = go.Scatter(x=df['MesNom'],
                            y=df['NewPatients'],
                            mode='lines',
                            name='Pacients nous',
                            stackgroup='one',
                            groupnorm='percent')

        trace_patients = go.Scatter(x=df['MesNom'],
                            y=df['Patients'],
                            mode='lines',
                            name='Pacients vells',
                            stackgroup='one')

        graph_title = 'Distribució nous pacients'
        data = [trace_new_patients, trace_patients]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                type='category',
            ),
            yaxis=dict(
                type='linear',
                range=[1, 100],
                dtick=20,
                ticksuffix='%'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'month evolution of new Patients per speciality'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_new_patients_per_speciality_per_month()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_new_patients_per_speciality_per_month():
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_nomEspecialitat as Spec, CONCAT(LEFT(f_month,4), "-", f_monthname) as MesNom, f_month as Mes, sum(f_newPatients) as NewPatients FROM dm2_newpatient_per_month_agenda GROUP BY f_nomEspecialitat, CONCAT(LEFT(f_month,4), "-", f_monthname), f_month'
        df = pd.read_sql(sql, connection)
        arraySpecs = df['Spec'].unique()
        df = df.set_index('Spec')
        data = list()
        for spec in arraySpecs:
            df_spec = pd.DataFrame(df.loc[df.index == spec, ['MesNom', 'Mes', 'NewPatients']])
            df_spec = df_spec.sort_values(['Mes'], ascending=[1])
            trace = go.Scatter(x=df_spec['MesNom'],
                y=df_spec['NewPatients'],
                mode='lines',
                name=spec,
                stackgroup='one',
                groupnorm='percent')
            data.append(trace)

        layout = go.Layout(
            title='Evolució de la distribució de nous pacients per especialitat',
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                type='category',
            ),
            yaxis=dict(
                type='linear',
                range=[1, 100],
                dtick=20,
                ticksuffix='%'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'New Patients per Speciality or Agenda'.
    You can choose to call by spec o agenda, but not both. If you set both values Spec is used.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_evolution_new_patients_per_spec(p_id_agenda='100')
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_evolution_new_patients_per_spec(p_id_especiality=None, p_id_agenda=None):
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_month as Mes, CONCAT(LEFT(f_month,4), "-", f_monthname) as MesNom, sum(f_newPatients) as NewPatients from dm2_newpatient_per_month_agenda WHERE '
        if (p_id_especiality is None or p_id_especiality == '') and p_id_agenda is None:
            p_id_especiality = 19# medicina general per defecte
        if (p_id_especiality is not None) and p_id_especiality != "":
            sql = sql + 'f_idEspecialitat=' + str(p_id_especiality) + ' '
        else:
            if (p_id_agenda is not None) and p_id_agenda != "":
                sql = sql + 'f_idAgenda=\'' + str(p_id_agenda) + '\' '
        sql = sql + 'GROUP BY f_month, CONCAT(LEFT(f_month,4), "-", f_monthname) '
        sql = sql + 'ORDER BY f_month ASC'
        df = pd.read_sql(sql, connection)
        if df.empty:
            return None
        trace_new_patients = go.Scatter(x=df['MesNom'],
                            y=df['NewPatients'],
                            mode='lines+markers',
                            name='Pacients nous')

        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['NewPatients'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression_new_patients = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='Tendencia nous pacients')

        graph_title = 'Evolució del número de pacients nous'
        if p_id_especiality is not None:
            graph_title = q.get_Spec_Name(p_id_especiality) + ': '+ graph_title
        if p_id_agenda is not None:
            graph_title = q.get_Agenda_Name(p_id_agenda) + ': '+ graph_title
        data = [trace_new_patients, trace_regression_new_patients]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                type='category',
            ),
            yaxis=dict(showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Distribution of new patients by speciality'.

    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_distribution_new_patients_per_spec('201801', '201812')
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param p_first_month: starting month of range values in YYYYMM format
    :param p_last_month: ending month of range values in YYYYMM format
    :rtype: string
"""
def plot_distribution_new_patients_per_spec(p_first_month, p_last_month):
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_nomEspecialitat as Spec, sum(f_newPatients) as NewPatients FROM datawarehouse.dm2_newpatient_per_month_agenda WHERE f_month >= '+str(p_first_month)+' and f_month <= '+str(p_last_month)+' GROUP BY f_nomEspecialitat ORDER BY sum(f_newPatients) DESC'
        df = pd.read_sql(sql, connection)
        trace_new_patients = go.Pie(labels=df['Spec'], values=df['NewPatients'])

        graph_title = 'Nous pacients per especialitat (Del ' + u.yyyymmToMonthName(p_first_month) + ' al ' + u.yyyymmToMonthName(p_last_month) + ')'
        data = [trace_new_patients]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                type='category',
            ),
            yaxis=dict(showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'New Patients per agenda'.
    Optionally, you can show by speciallity. If no speciality is set it shows whole data.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_first_blood_per_agenda('201801', '201812')
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param p_first_month: starting month of range values in YYYYMM format
    :param p_last_month: ending month of range values in YYYYMM format
    :param p_id_especiality: optional identifier of speciality
    :rtype: string
"""
def plot_first_blood_per_agenda(p_first_month, p_last_month, p_id_especiality=None):
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_nomAgenda as nomAgenda, sum(f_totalVisits) as Total, COUNT(*) as Patients, sum(f_totalVisits)/COUNT(*) as PerPatient FROM datawarehouse.dm_first_visit WHERE f_month between '+str(p_first_month)+' and '+str(p_last_month)
        if p_id_especiality is not None:
            sql = sql + ' AND f_idEspecialitat=' + str(p_id_especiality) + ' '
        sql = sql + ' GROUP BY f_nomAgenda'
        sql = sql + ' ORDER BY sum(f_totalVisits) DESC'
        df = pd.read_sql(sql, connection)
        trace_visits = go.Bar(x=df['nomAgenda'],
                            y=df['Total'],
                            name='Total visites al centre')

        trace_per_patient = go.Bar(x=df['nomAgenda'],
                            y=df['PerPatient'],
                            name='Mitjana per pacient')

        graph_title = 'Visites per captació en agenda (Del ' + u.yyyymmToMonthName(p_first_month) + ' al ' + u.yyyymmToMonthName(p_last_month) + ')'
        if p_id_especiality is not None:
            graph_title = q.get_Spec_Name(p_id_especiality) + ': ' + graph_title
        data = [trace_visits, trace_per_patient]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=12,
                                     color='black'),
            ),
            yaxis=dict(showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Last visits per month'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_last_visits_per_month()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_last_visits_per_month():
    try:
        connection = connections['datawarehouse']
        # we don't want to show future months, so we filter till past month
        now = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        last_month = str(now.year) + str(now.month+1).zfill(2)
        sql = 'SELECT f_lastmonth as Mes, CONCAT(LEFT(f_lastmonth,4), "-", f_lastmonthname) as MesNom, count(*) as Total FROM datawarehouse.dm_first_visit WHERE f_lastmonth < '+ last_month + ' GROUP BY f_lastmonth, CONCAT(LEFT(f_lastmonth,4), "-", f_lastmonthname) ORDER BY f_lastmonth ASC'
        df = pd.read_sql(sql, connection)
        trace_visits = go.Scatter(x=df['MesNom'],
                            y=df['Total'],
                            mode='lines+markers',
                            name='Ultimes visites per mes')
        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['Total'])
        predicted_y = pol_reg.predict(poly_reg.fit_transform(linear_x))
        trace_regression_visits = go.Scatter(x=df['MesNom'],
                            y=predicted_y,
                            mode='lines',
                            name='Tendencia')

        trace_omi_annotation = go.Scatter(x=["2017-Dec", "2017-Dec"],
                            y=[0, df['Total'].max()],
                            mode='lines',
                            name='Inici odontologia a OMI360',
                            line=dict(dash='dot'))

        data = [trace_visits, trace_regression_visits, trace_omi_annotation]
        layout = go.Layout(
            title='Evolució del número de últimes visites per mes',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'),
            yaxis=dict(titlefont=dict(family='Arial, sans-serif',
                                      size=18,
                                      color='lightgrey'),
                       showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Visits per patient'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_visits_per_patient()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_visits_per_patient():
    try:
        connection = connections['datawarehouse']
        df = pd.read_sql('SELECT f_numHistoria as Patient, f_totalVisits as Total FROM datawarehouse.dm_first_visit', connection)
        #max outliners to 50 for better visualization
        df[df['Total'] > 50] = 50
        trace_visits = go.Histogram(x=df['Total'],
                            name='Visites per pacient')
        data = [trace_visits]
        layout = go.Layout(
            title='Distribució del número de visites per pacient',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none',
                       title='Visites'),
            yaxis=dict(showticklabels=True,
                        title='Número de pacients',
                        tickformat='.0f',
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Distribution casual vs fidelizied'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_distribution_casual_vs_fidelizied()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_distribution_casual_vs_fidelizied():
    try:
        connection = connections['datawarehouse']
        sql = 'SELECT f_month as mes, CONCAT(LEFT(f_month,4), "-", f_monthname) as MesNom, f_casuals as casuals, f_fidelitzats as fidelitzats, f_visits_casuals as visitsCasuals, f_visits_fidelitzats as visitsFidelitzats FROM datawarehouse.dm2_stats_per_month ORDER BY f_month ASC'
        df = pd.read_sql(sql, connection)
        trace_casual = go.Scatter(x=df['MesNom'],
                            y=df['casuals'],
                            mode='lines',
                            name='Pacients casuals',
                            stackgroup='one',
                            groupnorm='percent')

        trace_fidelizied = go.Scatter(x=df['MesNom'],
                            y=df['fidelitzats'],
                            mode='lines',
                            name='Pacients fidelitzats',
                            stackgroup='one')

        data = [trace_casual, trace_fidelizied]
        layout = go.Layout(
            title='Distribució pacients casuals vs fidelitzats',
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                type='category',
            ),
            yaxis=dict(
                type='linear',
                range=[1, 100],
                dtick=20,
                ticksuffix='%'))
        fig = go.Figure(data=data, layout=layout)
        plotdiv_patients = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        trace_visits_casual = go.Scatter(x=df['MesNom'],
                            y=df['visitsCasuals'],
                            mode='lines',
                            name='Visites casuals',
                            stackgroup='one',
                            groupnorm='percent')

        trace_visits_fidelizied = go.Scatter(x=df['MesNom'],
                            y=df['visitsFidelitzats'],
                            mode='lines',
                            name='Visites fidelitzats',
                            stackgroup='one')

        data = [trace_visits_casual, trace_visits_fidelizied]
        layout = go.Layout(
            title='Distribució visites casuals vs fidelitzats',
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                tickangle=45,
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                type='category',
            ),
            yaxis=dict(
                type='linear',
                range=[1, 100],
                dtick=20,
                ticksuffix='%'))
        fig = go.Figure(data=data, layout=layout)
        plotdiv_visits = py.offline.plot(fig, include_plotlyjs=False, output_type='div')
        return plotdiv_patients, plotdiv_visits

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Generates a offline plotly plot with the graph 'Distance to last visit'.
    Return HTML div code that builds the graph. It is necessary to include 'plotly.js'
    in your html file.

    usage::

        >>> import plots
        >>> plot = plot_distance_to_lastmonth()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot})

    :param: None
    :rtype: string
"""
def plot_distance_to_lastmonth():
    try:
        connection = connections['datawarehouse']
        df = pd.read_sql('SELECT f_numHistoria as Patient, PERIOD_DIFF(IF(f_lastmonth=f_month,EXTRACT(YEAR_MONTH FROM CURRENT_DATE()),f_lastmonth), f_month) as mesos FROM datawarehouse.dm_first_visit', connection)

        df = df[df['mesos']>0]
        trace_distance = go.Histogram(x=df['mesos'],
                            name='Mesos des de última visita')

        data = [trace_distance]
        layout = go.Layout(
            title='Conteig dels mesos que fa que no ve cada pacient',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=45,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none',
                       title='Mesos des de última visita'),
            yaxis=dict(showticklabels=True,
                        title='Número de pacients',
                        tickformat='.0f',
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        return py.offline.plot(fig, include_plotlyjs=False, output_type='div')

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Callcenter plots to analyse performance.
    usage::

        >>> import plots
        >>> plots = plots_callcenter_period('2018/01/01', '2018/01/31')
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot[1]})

    :param p_date_ini: string representation of starting date in YYYY/MM/DD format
    :param p_date_fin: string representation of ending date in YYYY/MM/DD format
    :rtype: array of plots
"""
def plots_callcenter_period (p_date_ini, p_date_fin):
    try:

        connection = connections['datawarehouse']
        # format date to use in a between condition: YYYYMMDD
        date_ini = datetime.datetime.strptime(str(p_date_ini), "%d/%m/%Y").strftime("%Y/%m/%d")
        date_fin = datetime.datetime.strptime(str(p_date_fin), "%d/%m/%Y").strftime("%Y/%m/%d")
        sql = "SELECT f_hour, sum(f_total) as total, sum(f_answered) as answered, sum(f_not_answered) as not_answered, if(sum(f_answered)>0,sum(f_not_answered)/sum(f_answered),sum(f_not_answered)) as overcall_factor FROM dm3_callcenter_general WHERE f_day BETWEEN \'"+date_ini+"\' AND \'"+date_fin+"\' and f_dst_id='6000' and f_hour between '07' and '23' GROUP BY f_hour ORDER BY f_hour ASC"
        df = pd.read_sql(sql, connection)

        if df.empty:
            return "No hi han dades en el periode triat.", None, None, None, None, None

        trace_answered = go.Scatter(x=df['f_hour'],
                            y=df['answered'],
                            mode='lines',
                            name='Contestades',
                            stackgroup='one',
                            fillcolor='#81d386',
                            line = dict(
                                color = ('#81d386'),),
                            hovertemplate = '%{y:.2f}%',
                            groupnorm='percent')

        trace_not_answered = go.Scatter(x=df['f_hour'],
                            y=df['not_answered'],
                            mode='lines',
                            name='No contestades',
                            hovertemplate = '%{y:.2f}%',
                            line = dict(
                                color = ('#f28282'),),
                            fillcolor= '#f28282',
                            stackgroup='one')

        graph_title = 'Distribució contestades vs no contestades'
        data = [trace_answered, trace_not_answered]
        layout = go.Layout(
            title=graph_title,
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                ticksuffix='h',
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                tickmode='linear',
            ),
            yaxis=dict(type='linear',
                    range=[1, 100],
                    dtick=20,
                    ticksuffix='%')
            )
        fig = go.Figure(data=data, layout=layout)
        plot_distrib = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        trace_abs_lost_calls = go.Bar(x=df['f_hour'],
                        y=df['not_answered'],
                        name='total no agafades')
        layout = go.Layout(
            title='Quantitat trucades no agafades',
            titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
            showlegend=True,
            xaxis=dict(
                showticklabels=True,
                ticksuffix='h',
                tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                tickmode='linear',
            ),
            )
        data=[trace_abs_lost_calls]
        fig = go.Figure(data=data, layout=layout)
        plot_abs_values = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        df = pd.read_sql("select f_week_day_order, f_week_day, f_hour, sum(f_not_answered) as not_answered, sum(f_total) as total from dm3_callcenter_general where f_day BETWEEN \'"+date_ini+"\' AND \'"+date_fin+"\' and f_dst_id='6000' and f_hour between '07' and '22' group by f_week_day_order, f_week_day, f_hour order by f_week_day_order ASC, f_hour ASC", connection)

        days = df['f_week_day'].unique()
        hours = sorted(df['f_hour'].unique())
        values = []
        for hour in hours:
            line = []
            for day in days:
                v = df.loc[(df['f_week_day'] == day) & (df['f_hour'] == hour), 'not_answered'].values
                if v.size >0:
                    line.append(v[0])
                else:
                    line.append(0)
            values.append(line)

        trace_heatmap_no_answer = go.Heatmap(z=values, x=days, y=hours, colorscale='Reds')
        data = [trace_heatmap_no_answer]
        layout = go.Layout(
            title='No contestades (valor absolut)',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            yaxis=dict(
                    showticklabels=True,
                    ticksuffix='h',
                    tickfont=dict(family='Old Standard TT, serif',
                                         size=14,
                                         color='black'),
                    tickmode='linear',
                ),
            )
        fig = go.Figure(data=data, layout=layout)
        plot_heatmap_no_answer = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        # total calls
        total_values = []
        for hour in hours:
            line = []
            for day in days:
                v = df.loc[(df['f_week_day'] == day) & (df['f_hour'] == hour), 'total'].values
                if v.size >0:
                    line.append(v[0])
                else:
                    line.append(0)
            total_values.append(line)

        trace_heatmap_total = go.Heatmap(z=total_values, x=days, y=hours, colorscale='Blues', reversescale=True)
        data = [trace_heatmap_total]
        layout = go.Layout(
            title='Rebudes (valor absolut)',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            yaxis=dict(
                    showticklabels=True,
                    ticksuffix='h',
                    tickfont=dict(family='Old Standard TT, serif',
                                         size=14,
                                         color='black'),
                    tickmode='linear',
                ),
            )
        fig = go.Figure(data=data, layout=layout)
        plot_heatmap_total = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        df = pd.read_sql("select f_day, f_hour, sum(f_not_answered) as not_answered, sum(f_total) as total from dm3_callcenter_general where f_day BETWEEN \'"+date_ini+"\' AND \'"+date_fin+"\' and f_dst_id='6000' and f_hour between '07' and '22' group by f_day, f_hour order by f_day ASC, f_hour ASC", connection)

        days = df['f_day'].unique()
        hours = sorted(df['f_hour'].unique())
        values_day = []
        values_total = []

        for hour in hours:
            line = []
            line_total = []
            for day in days:
                v = df.loc[(df['f_day'] == day) & (df['f_hour'] == hour), 'not_answered'].values
                v_total = df.loc[(df['f_day'] == day) & (df['f_hour'] == hour), 'total'].values
                if v.size >0:
                    line.append(v[0])
                else:
                    line.append(0)
                if v_total.size >0:
                    line_total.append(v_total[0])
                else:
                    line_total.append(0)
            values_day.append(line)
            values_total.append(line_total)
        trace_heatmap_per_day_no_answer = go.Heatmap(z=values_day, x=days, y=hours, colorscale='Reds')
        data = [trace_heatmap_per_day_no_answer]
        layout = go.Layout(
            title='No contestades per dia (valor absolut)',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            yaxis=dict(
                    showticklabels=True,
                    ticksuffix='h',
                    tickfont=dict(family='Old Standard TT, serif',
                                         size=14,
                                         color='black'),
                    tickmode='linear',
                ),
            )
        fig = go.Figure(data=data, layout=layout)
        plot_heatmap_per_day_no_answer = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        trace_heatmap_per_day_total = go.Heatmap(z=values_total, x=days, y=hours, colorscale='Blues', reversescale=True)
        data = [trace_heatmap_per_day_total]
        layout = go.Layout(
            title='Rebudes per dia (valor absolut)',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            yaxis=dict(
                    showticklabels=True,
                    ticksuffix='h',
                    tickfont=dict(family='Old Standard TT, serif',
                                         size=14,
                                         color='black'),
                    tickmode='linear',
                ),
            )
        fig = go.Figure(data=data, layout=layout)
        plot_heatmap_per_day_total = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        return plot_distrib, plot_abs_values, plot_heatmap_no_answer, plot_heatmap_total, plot_heatmap_per_day_no_answer, plot_heatmap_per_day_total

    except Error as e:
        print("Error while connecting to MySQL", e)


""" Callcenter plots representing evolution
    usage::

        >>> import plots
        >>> plots = plots_callcenter_evo()
        >>> render (request, 'someViewWithPlot.html', {'plot_name': plot[1]})

    :param: None
    :rtype: array of plots
"""
def plots_callcenter_evo():
    try:
        connection = connections['datawarehouse']
        current_month = datetime.date.today().strftime('%Y%m')
        sql = 'SELECT f_month, sum(f_total) as total, sum(f_answered) as answered, sum(f_not_answered) as not_answered, sum(f_answered)/sum(f_total) as percent_answered, sum(f_not_answered)/sum(f_total) as percent_not_answered FROM datawarehouse.dm3_callcenter_general WHERE f_month < ' + current_month +' GROUP BY f_month ORDER BY f_month ASC'

        df = pd.read_sql(sql, connection)
        df['f_month_order'] = np.arange(len(df))
        trace_total = go.Scatter(x=df['f_month_order'],
                            y=df['total'],
                            mode='lines',
                            name='Rebudes per mes',
                            line = dict(
                                color = ('blue'),
                                dash = 'solid'),)
        trace_answered = go.Scatter(x=df['f_month_order'],
                            y=df['answered'],
                            mode='lines',
                            name='Contestades per mes',
                            line = dict(
                                color = ('green'),
                                dash = 'solid',),)
        trace_not_answered = go.Scatter(x=df['f_month_order'],
                            y=df['not_answered'],
                            mode='lines',
                            name='No contestades per mes',
                            line = dict(
                                color = ('red'),
                                dash = 'solid',),)
        linear_x = np.r_[0:len(df)]
        linear_x = np.arange(0, len(df)).reshape(-1, 1)
        poly_reg = PolynomialFeatures(degree=4)
        X_poly = poly_reg.fit_transform(linear_x)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, df['total'])
        predicted_y_total = pol_reg.predict(poly_reg.fit_transform(linear_x))
        pol_reg.fit(X_poly, df['answered'])
        predicted_y_answered = pol_reg.predict(poly_reg.fit_transform(linear_x))
        pol_reg.fit(X_poly, df['not_answered'])
        predicted_y_not_answered = pol_reg.predict(poly_reg.fit_transform(linear_x))

        trace_regression_total = go.Scatter(x=df['f_month_order'],
                            y=predicted_y_total,
                            mode='lines',
                            name='Tendencia trucades rebudes',
                            line = dict(
                                color = ('blue'),
                                dash = 'dot'),)
        trace_regression_answered = go.Scatter(x=df['f_month_order'],
                            y=predicted_y_answered,
                            mode='lines',
                            name='Tendencia trucades contestades',
                            line = dict(
                                color = ('green'),
                                dash = 'dot'),)
        trace_regression_not_answered = go.Scatter(x=df['f_month_order'],
                            y=predicted_y_not_answered,
                            mode='lines',
                            name='Tendencia trucades no contestades',
                            line = dict(
                                color = ('red'),
                                dash = 'dot'),)

        data = [trace_total, trace_regression_total, trace_answered, trace_regression_answered, trace_not_answered, trace_regression_not_answered]
        layout = go.Layout(
            title='Evolució del número de trucades per mes',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=60,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=10,
                                     color='black'),
                       showexponent='none',
                       tickmode = 'array',
                        tickvals = df['f_month_order'],
                        ticktext = df['f_month']),
            yaxis=dict(titlefont=dict(family='Arial, sans-serif',
                                      size=18,
                                      color='lightgrey'),
                       showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        plot_absolute = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        trace_visits_casual = go.Scatter(x=df['f_month_order'],
                            y=df['percent_answered'],
                            mode='lines',
                            name='Contestades',
                            stackgroup='one',
                            groupnorm='percent')

        trace_visits_fidelizied = go.Scatter(x=df['f_month_order'],
                            y=df['percent_not_answered'],
                            mode='lines',
                            name='No contestades',
                            stackgroup='one')
        data = [trace_visits_casual, trace_visits_fidelizied]
        layout = go.Layout(
            title='Distribució contestades vs no contestades mes a mes',
            titlefont=dict(family='Arial, sans-serif',
                           size=24,
                           color='green'),
            xaxis=dict(showticklabels=True,
                       tickangle=60,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=10,
                                     color='black'),
                       showexponent='none',
                       tickmode = 'array',
                        tickvals = df['f_month_order'],
                        ticktext = df['f_month']),
            yaxis=dict(titlefont=dict(family='Arial, sans-serif',
                                      size=18,
                                      color='lightgrey'),
                       showticklabels=True,
                       tickfont=dict(family='Old Standard TT, serif',
                                     size=14,
                                     color='black'),
                       showexponent='none'))
        fig = go.Figure(data=data, layout=layout)
        plot_distrib_percent = py.offline.plot(fig, include_plotlyjs=False, output_type='div')

        return plot_absolute, plot_distrib_percent, plot_absolute

    except Error as e:
        print("Error while connecting to MySQL", e)


def plots_ext_performance(p_date_ini, p_date_fin):
    try:
        connection = connections['datawarehouse']
        # format date to use in a between condition: YYYYMMDD
        date_ini = datetime.datetime.strptime(str(p_date_ini), "%d/%m/%Y").strftime("%Y/%m/%d")
        date_fin = datetime.datetime.strptime(str(p_date_fin), "%d/%m/%Y").strftime("%Y/%m/%d")
        sql = "SELECT f_extension as extension, sum(f_answered) as answered, sum(f_spoken_time) as spoken_time, sum(f_spoken_time)/sum(f_answered) as time_per_call FROM dm3_callcenter_per_extension WHERE f_day BETWEEN \'"+date_ini+"\' AND \'"+date_fin+"\' and f_extension IN (100, 101, 102, 104, 111, 112) GROUP BY f_extension"
        df = pd.read_sql(sql, connection)

        lines = []
        line = {}
        calls = 0
        spoken_time = 0
        time_per_call = 0
        total = 0
        for index, row in df.iterrows():
            calls += row[1]
            spoken_time += row[2]
            time_per_call += row[3]
            total += 1
            line = {'extension': row[0], 'answered': f'{row[1]:10.0f}', 'spoken_time': f'{row[2]/3600:10.2f}', 'time_per_call': f'{row[3]/60:10.2f}'}
            lines.append(line)
        # add averages
        if total > 0:
            line = {'extension': 'promig', 'answered': f'{calls/total:10.0f}', 'spoken_time': f'{spoken_time/(3600*total):10.2f}', 'time_per_call': f'{time_per_call/(60*total):10.2f}'}
            lines.append(line)

        sql = "SELECT f_extension as extension, f_day, f_hour, sum(f_answered) as answered, sum(f_spoken_time) as spoken_time, sum(f_spoken_time)/sum(f_answered) as time_per_call FROM dm3_callcenter_per_extension WHERE f_day BETWEEN \'"+date_ini+"\' AND \'"+date_fin+"\' and f_extension IN (100, 101, 102, 104, 111, 112) GROUP BY f_extension, f_day, f_hour ORDER BY f_extension, f_day, f_hour"
        df = pd.read_sql(sql, connection)
        extensions = sorted(df['extension'].unique())
        days = sorted(df['f_day'].unique())
        hours = sorted(df['f_hour'].unique())

        plots = []
        for extension in extensions:
            values_day = []

            for hour in hours:
                line = []
                for day in days:
                    v = df.loc[(df['extension'] == extension) & (df['f_day'] == day) & (df['f_hour'] == hour), 'answered'].values
                    if v.size >0:
                        line.append(v[0])
                    else:
                        line.append(0)
                values_day.append(line)
            trace_heatmap_per_extension = go.Heatmap(z=values_day, x=days, y=hours, colorscale='Reds', name=extension)
            graph_title = 'Trucades ateses per l\'extensió ' + extension
            layout = go.Layout(
                title=graph_title,
                titlefont=dict(family='Arial, sans-serif',
                               size=24,
                               color='green'),
                yaxis=dict(
                        showticklabels=True,
                        ticksuffix='h',
                        tickfont=dict(family='Old Standard TT, serif',
                                             size=14,
                                             color='black'),
                        tickmode='linear',
                    ),
                )
            heatmap_data = [trace_heatmap_per_extension]
            fig = go.Figure(data=heatmap_data, layout=layout)
            plots.append(py.offline.plot(fig, include_plotlyjs=False, output_type='div'))

        return lines, plots
    except Error as e:
        print("Error while connecting to MySQL", e)
