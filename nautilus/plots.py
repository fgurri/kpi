import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly as py
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import configparser
import nautilus.utils as u
import nautilus.queries as q

# read properties on project root
config = configparser.RawConfigParser()
config.read(r'nautilus.properties')


def plot_visits_per_month():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_month as mes, CONCAT(f_year, "-", f_monthname) as mesnom, sum(f_count) as total FROM datawarehouse.dm1_visits_per_agenda GROUP BY f_month,  CONCAT(f_year, "-", f_monthname)'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Mes', 1: 'MesNom', 2: 'Total'})
            df = df.sort_values(['Mes'], ascending=[1])
            trace0 = go.Scatter(x=df['MesNom'],
                                y=df['Total'],
                                mode='lines+markers',
                                name='Visites per mes')
            index_start_odonto_omi = list(df['MesNom']).index("2017-Dec")
            value_start_odonto_omi = df['Total'].get(index_start_odonto_omi)

            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['Total'])
            trace1 = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia')

            trace2 = go.Scatter(x=["2017-Dec", "2017-Dec"],
                                y=[0, df['Total'].max()],
                                mode='lines',
                                name='Inici odontologia a OMI360',
                                line=dict(dash='dot'))

            data = [trace0, trace1, trace2]
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
                yaxis=dict(title='Visites en milers',
                           titlefont=dict(family='Arial, sans-serif',
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_distribution_visits_per_speciality(p_firstmonth, p_lastmonth):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
              'SELECT f_nomEspecialitat as spec, sum(f_count) as total FROM datawarehouse.dm1_visits_per_agenda WHERE f_month >= '+str(p_firstmonth)+' and f_month <= '+str(p_lastmonth)+' GROUP BY f_nomEspecialitat'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Spec', 1: 'Total'})
            df = df.sort_values(['Total'], ascending=[0])

            trace0 = go.Pie(labels=df['Spec'], values=df['Total'])


            graphTitle = 'Distribució visites per especialitat (Del ' + u.yyyymmToMonthName(p_firstmonth) + ' al ' + u.yyyymmToMonthName(p_lastmonth) + ')'
            data = [trace0]
            layout = go.Layout(
                  title=graphTitle,
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
                  yaxis=dict(title='Visites en milers',
                             titlefont=dict(family='Arial, sans-serif',
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_visits_per_month_speciality(p_idEspeciality=None, p_idAgenda=None):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'SELECT CONCAT(f_year, "-", f_monthname) as mesnom, f_month, sum(f_count) as total FROM datawarehouse.dm1_visits_per_agenda WHERE '
            if p_idEspeciality is None and p_idAgenda is None:
                p_idEspeciality=19 # medicina general per defecte
            if (not p_idEspeciality is None) and p_idEspeciality != "":
                sql = sql + 'f_idEspecialitat='+str(p_idEspeciality)+' '
            else:
                if (not p_idAgenda is None) and p_idAgenda != "":
                    sql = sql + 'f_idAgenda=\''+str(p_idAgenda)+'\' '
            sql = sql + 'GROUP BY CONCAT(f_year, "-", f_monthname), f_month'
            cursor.execute(sql)

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'MesNom', 1: 'f_month', 2: 'Total'})
            df = df.sort_values(['f_month'], ascending=[1])
            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['Total'])
            trace1 = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia Especialitat')

            trace0 = go.Scatter(x=df['MesNom'],
                                y=df['Total'],
                                mode='lines+markers',
                                name='Visites per mes')

            graphTitle = 'Evolució mensual de visites'
            if not p_idEspeciality is None:
                graphTitle = q.get_Spec_Name(p_idEspeciality) + ': '+ graphTitle
            if not p_idAgenda is None:
                graphTitle = q.get_Agenda_Name(p_idAgenda) + ': '+ graphTitle
            data = [trace0, trace1]
            layout = go.Layout(
                title=graphTitle,
                titlefont=dict(family='Arial, sans-serif', size=24, color='green'),
                xaxis=dict(showticklabels=True,
                           tickangle=45,
                           tickfont=dict(family='Old Standard TT, serif',
                                         size=14,
                                         color='black'),
                           showexponent='none'),
                yaxis=dict(title='Visites en milers',
                           titlefont=dict(family='Arial, sans-serif',
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_frequency_per_agenda(p_idAgenda):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'SELECT CONCAT(f_year, "-", f_monthname) as mesnom, f_month, f_count/f_patients as rep FROM datawarehouse.dm1_visits_per_agenda WHERE f_idAgenda=\''+str(p_idAgenda)+'\''
            cursor.execute(sql)

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'MesNom', 1: 'f_month', 2: 'rep'})
            df = df.sort_values(['f_month'], ascending=[1])

            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            trace0 = go.Scatter(x=df['MesNom'],
                                y=df['rep'],
                                mode='lines+markers',
                                name='repetitivitat')

            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['rep'])
            trace2 = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='regressio repetitivitat')

            graphTitle = q.get_Agenda_Name(p_idAgenda) + ': Freqüentació'
            data = [trace0, trace2]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_patients_per_month():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_month, CONCAT(LEFT(f_month, 4), "-", f_monthname) as f_monthname, f_patients, f_new_patients FROM datawarehouse.dm2_patients_per_month'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Mes', 1: 'MesNom', 2: 'Patients', 3: 'NewPatients'})
            df = df.sort_values(['Mes'], ascending=[1])
            trace0_total = go.Scatter(x=df['MesNom'],
                                y=df['Patients'],
                                mode='lines+markers',
                                name='Total pacients')

            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['Patients'])
            trace1_total = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia total pacients')

            trace2 = go.Scatter(x=["2017-Dec", "2017-Dec"],
                                y=[0, df['Patients'].max()],
                                mode='lines',
                                name='Inici odontologia a OMI360',
                                line=dict(dash='dot'))

            graphTitle = 'Pacients per mes'
            data = [trace0_total, trace1_total, trace2]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_new_patients_per_month():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_month, CONCAT(LEFT(f_month, 4), "-", f_monthname) as f_monthname, f_patients, f_new_patients FROM datawarehouse.dm2_patients_per_month'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Mes', 1: 'MesNom', 2: 'Patients', 3: 'NewPatients'})
            df = df.sort_values(['Mes'], ascending=[1])
            trace0_new = go.Scatter(x=df['MesNom'],
                                y=df['NewPatients'],
                                mode='lines+markers',
                                name='Pacients nous')

            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['NewPatients'])
            trace1_new = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia nous pacients')

            trace2 = go.Scatter(x=["2017-Dec", "2017-Dec"],
                                y=[0, df['NewPatients'].max()],
                                mode='lines',
                                name='Inici odontologia a OMI360',
                                line=dict(dash='dot'))

            graphTitle = 'Pacients nous per mes'
            data = [trace0_new, trace1_new, trace2]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_distribution_new_patients():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_month, CONCAT(LEFT(f_month, 4), "-", f_monthname) as f_monthname, f_patients-f_new_patients as f_patients, f_new_patients FROM datawarehouse.dm2_patients_per_month'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Mes', 1: 'MesNom', 2: 'Patients', 3: 'NewPatients'})
            df = df.sort_values(['Mes'], ascending=[1])
            trace0_new = go.Scatter(x=df['MesNom'],
                                y=df['NewPatients'],
                                mode='lines',
                                name='Pacients nous',
                                stackgroup='one',
                                groupnorm='percent')

            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['NewPatients'])
            trace1_new = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia nous pacients')

            trace0_total = go.Scatter(x=df['MesNom'],
                                y=df['Patients'],
                                mode='lines',
                                name='Pacients vells',
                                stackgroup='one')

            pol_reg.fit(X_poly, df['Patients'])
            trace1_total = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia total pacients')

            trace2 = go.Scatter(x=["2017-Dec", "2017-Dec"],
                                y=[0, df['NewPatients'].max()],
                                mode='lines',
                                name='Inici odontologia a OMI360',
                                line=dict(dash='dot'))

            graphTitle = 'Distribució nous pacients'
            data = [trace0_new, trace0_total]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_new_patients_per_speciality_per_month():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_nomEspecialitat, CONCAT(LEFT(f_month,4), "-", f_monthname) as mesnom, f_month, sum(f_newPatients) as total FROM dm2_newpatient_per_month_agenda GROUP BY f_nomEspecialitat, CONCAT(LEFT(f_month,4), "-", f_monthname), f_month'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Spec', 1: 'MesNom', 2: 'Mes', 3: 'NewPatients'})
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_evolution_new_patients_per_spec(p_idEspeciality=None, p_idAgenda=None):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'SELECT f_month, CONCAT(LEFT(f_month,4), "-", f_monthname) as mesnom, sum(f_newPatients) as total from dm2_newpatient_per_month_agenda WHERE '
            if p_idEspeciality is None and p_idAgenda is None:
                p_idEspeciality=19 # medicina general per defecte
            if (not p_idEspeciality is None) and p_idEspeciality != "":
                sql = sql + 'f_idEspecialitat='+str(p_idEspeciality)+' '
            else:
                if (not p_idAgenda is None) and p_idAgenda != "":
                    sql = sql + 'f_idAgenda=\''+str(p_idAgenda)+'\' '
            sql = sql + 'GROUP BY f_month, CONCAT(LEFT(f_month,4), "-", f_monthname)'
            print(sql)
            cursor.execute(sql)

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Mes', 1: 'MesNom', 2: 'NewPatients'})
            df = df.sort_values(['Mes'], ascending=[1])
            trace0_new = go.Scatter(x=df['MesNom'],
                                y=df['NewPatients'],
                                mode='lines+markers',
                                name='Pacients nous')

            linear_x = np.r_[0:len(df)]
            linear_x = np.arange(0, len(df)).reshape(-1, 1)
            poly_reg = PolynomialFeatures(degree=4)
            X_poly = poly_reg.fit_transform(linear_x)
            pol_reg = LinearRegression()
            pol_reg.fit(X_poly, df['NewPatients'])
            trace1_new = go.Scatter(x=df['MesNom'],
                                y=pol_reg.predict(poly_reg.fit_transform(linear_x)), mode='lines',name='Tendencia nous pacients')

            graphTitle = 'Evolució del número de pacients nous'
            if not p_idEspeciality is None:
                graphTitle = q.get_Spec_Name(p_idEspeciality) + ': '+ graphTitle
            if not p_idAgenda is None:
                graphTitle = q.get_Agenda_Name(p_idAgenda) + ': '+ graphTitle
            data = [trace0_new, trace1_new]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_distribution_new_patients_per_spec(p_firstmonth, p_lastmonth):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_nomEspecialitat, sum(f_newPatients) as total FROM datawarehouse.dm2_newpatient_per_month_agenda WHERE f_month >= '+str(p_firstmonth)+' and f_month <= '+str(p_lastmonth)+' GROUP BY f_nomEspecialitat'
            )
            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'Especialitat', 1: 'NewPatients'})
            df = df.sort_values(['NewPatients'], ascending=[0])
            trace0_new = go.Pie(labels=df['Especialitat'], values=df['NewPatients'])

            graphTitle = 'Distribució nous pacients per especialitat (Del ' + u.yyyymmToMonthName(p_firstmonth) + ' al ' + u.yyyymmToMonthName(p_lastmonth) + ')'
            data = [trace0_new]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def plot_first_blood_per_agenda(p_firstmonth, p_lastmonth, p_idEspeciality=None):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'SELECT f_nomAgenda, sum(f_totalVisits) as visits, COUNT(*) as patients, sum(f_totalVisits)/COUNT(*) as visits_per_patient FROM datawarehouse.dm_first_visit WHERE f_month between '+str(p_firstmonth)+' and '+str(p_lastmonth)
            if not p_idEspeciality is None:
                sql = sql + ' AND f_idEspecialitat='+str(p_idEspeciality)+' '
            sql = sql + ' GROUP BY f_nomAgenda'
            cursor.execute(sql)
            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'nomAgenda', 1: 'Total', 2: 'Patients', 3: 'PerPatient'})
            df = df.sort_values(['Total'], ascending=[0])
            trace0 = go.Bar(x=df['nomAgenda'],
                                y=df['Total'],
                                name='Total visites al centre')

            trace1 = go.Bar(x=df['nomAgenda'],
                                y=df['PerPatient'],
                                name='Mitjana per pacient')

            graphTitle = 'Visites per captació en agenda (Del ' + u.yyyymmToMonthName(p_firstmonth) + ' al ' + u.yyyymmToMonthName(p_lastmonth) + ')'
            if not p_idEspeciality is None:
                graphTitle = q.get_Spec_Name(p_idEspeciality) + ': '+ graphTitle
            data = [trace0, trace1]
            layout = go.Layout(
                title=graphTitle,
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
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()
