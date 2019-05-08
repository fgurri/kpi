import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly as py
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np
import configparser

# read properties on project root
config = configparser.RawConfigParser()
config.read(r'nautilus.properties')


def generate_pm():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
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

            linear_x = np.r_[0:len(rows)]
            linear_x = np.arange(0, len(rows)).reshape(-1, 1)
            linear_regressor = LinearRegression(
            )  # create object for the class
            linear_regressor.fit(linear_x,
                                 df['Total'])  # perform linear regression
            linear_y = linear_regressor.predict(linear_x)  # make predictions
            trace1 = go.Scatter(x=df['MesNom'],
                                y=linear_y,
                                mode='lines',
                                name='Tendencia')

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


def generate_pcpe():
  try:
      connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
      if connection.is_connected():
          db_Info = connection.get_server_info()
          cursor = connection.cursor()
          cursor.execute(
              'SELECT f_nomEspecialitat as spec, sum(f_count) as total FROM datawarehouse.dm1_visits_per_agenda WHERE f_year=2019 GROUP BY f_nomEspecialitat'
          )

          rows = cursor.fetchall()
          df = pd.DataFrame([[ij for ij in i] for i in rows])
          df = df.rename(columns={0: 'Spec', 1: 'Total'})
          df = df.sort_values(['Total'], ascending=[0])

          trace0 = go.Bar(x=df['Spec'], y=df['Total'])

          data = [trace0]
          layout = go.Layout(
              title='Total visites per especialitat',
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


def generate_pepm(p_idEspeciality):
    try:
        print(config.get('DatabaseSection', 'database.host'))
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT CONCAT(f_year, "-", f_monthname) as mesnom, sum(f_count) as total FROM datawarehouse.dm1_visits_per_agenda WHERE f_idEspecialitat='+str(p_idEspeciality)+' GROUP BY CONCAT(f_year, "-", f_monthname)'
            )

            rows = cursor.fetchall()
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df = df.rename(columns={0: 'MesNom', 1: 'Total'})
            df = df.sort_values(['MesNom'], ascending=[1])

            cursor.execute(
                'SELECT CONCAT(f_year, "-", f_monthname) as mesnom, sum(f_count) as total FROM datawarehouse.dm1_visits_per_agenda GROUP BY CONCAT(f_year, "-", f_monthname)'
            )
            rows_all = cursor.fetchall()
            df_all = pd.DataFrame([[ij for ij in i] for i in rows_all])
            df_all = df_all.rename(columns={0: 'MesNom', 1: 'Total'})
            df_all = df_all.sort_values(['MesNom'], ascending=[1])

            linear_x = np.r_[0:len(rows)]
            linear_x = np.arange(0, len(rows)).reshape(-1, 1)
            linear_regressor = LinearRegression(
            )  # create object for the class
            linear_regressor.fit(linear_x,
                                 df['Total'])  # perform linear regression
            linear_y = linear_regressor.predict(linear_x)  # make predictions
            trace1 = go.Scatter(x=df['MesNom'],
                                y=linear_y,
                                mode='lines',
                                name='Tendencia Especialitat')
            linear_x_all = np.r_[0:len(rows_all)]
            linear_x_all = np.arange(0, len(rows_all)).reshape(-1, 1)
            linear_regressor_all = LinearRegression(
            )  # create object for the class
            linear_regressor_all.fit(
                linear_x_all, df_all['Total'])  # perform linear regression
            linear_y_all = linear_regressor_all.predict(
                linear_x_all)  # make predictions
            # linear_y_all = linear_y_all - (linear_regressor_all.intercept_ - linear_regressor.intercept_)
            trace1_all = go.Scatter(x=df_all['MesNom'],
                                    y=linear_y_all,
                                    mode='lines',
                                    name='Tendencia Global')
            trace0 = go.Scatter(x=df['MesNom'],
                                y=df['Total'],
                                mode='lines+markers',
                                name='Visites per mes')

            data = [trace0, trace1]
            layout = go.Layout(
                title='Evolució visites de Medicina General',
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
