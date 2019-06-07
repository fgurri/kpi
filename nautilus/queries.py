import configparser

import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np

import nautilus.utils as u

# read properties on project root
config = configparser.RawConfigParser()
config.read(r'nautilus.properties')

""" Generates an array of all specialities

    usage::

        >>> import queries
        >>> spec_array = get_Specialities()
        >>> for spec in spec_array:
        >>>     print(spec.id + ': ' + spec.name)

    :param:
    :rtype: array of tuples {'id': id, 'name': name}
"""
def get_Specialities():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_idEspecialitat, f_nomEspecialitat FROM datawarehouse.dm_especialitats ORDER BY f_nomEspecialitat ASC'
            )
            rows = cursor.fetchall()
            lines = []
            line = {}
            for result in rows:
                line = {'id': result[0], 'name': result[1]}
                lines.append(line)
                line = {}
            return lines

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Generates an array of all agendas

    usage::

        >>> import queries
        >>> spec_array = get_Agendas()
        >>> for agenda in agenda_array:
        >>>     print(agenda.id + ': ' + agenda.name)

    :param:
    :rtype: array of tuples {'id': id, 'name': name, 'spec_id': spec_id, 'spec_name': spec_name}
"""
def get_Agendas():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT ea.f_idAgenda, ea.f_nomAgenda, ea.f_idEspecialitat, e.f_nomEspecialitat FROM datawarehouse.dm_especialitat_agenda ea LEFT OUTER JOIN dm_especialitats e ON e.f_idEspecialitat = ea.f_idEspecialitat ORDER BY f_nomAgenda ASC'
            )
            rows = cursor.fetchall()
            lines = []
            line = {}
            for result in rows:
                spec_name = result[3]
                spec_id = result[2]
                if spec_name is None:
                    spec_name = ''
                    spec_id = ''
                line = {'id': result[0], 'name': result[1], 'spec_id': spec_id, 'spec_name': spec_name}
                lines.append(line)
                line = {}
            return lines

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Generates an array of all months in table dm2_newpatient_per_month_agenda.
    Months id are in format YYYYMM and the name is YYYY concat with the first
    three character of english month name. For example: 2018-Jan

    usage::

        >>> import queries
        >>> month_array = get_Months()
        >>> for month in month_array:
        >>>     print(month.id + ': ' + month.name)

    :param:
    :rtype: array of tuples {'id': id, 'name': name}
"""
def get_Months():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT distinct f_month, CONCAT(LEFT(f_month, 4), \'-\', f_monthname) from dm2_newpatient_per_month_agenda order by f_month'
            )
            rows = cursor.fetchall()
            lines = []
            line = {}
            for result in rows:
                line = {'id': result[0], 'name': result[1]}
                lines.append(line)
                line = {}
            return lines

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Generates a list of all months in table dm2_newpatient_per_month_agenda.
    Months are in format YYYYMM.

    usage::

        >>> import queries
        >>> month_list = get_month_list()
        >>> for month in month_list:
        >>>     print(month)

    :param:
    :rtype: list of YYYYMM months
"""
def get_month_list():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT distinct f_month from dm2_newpatient_per_month_agenda order by f_month'
            )
            monthlist = [item[0] for item in cursor.fetchall()]
            return monthlist

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Retrieves the speciality name from table dm_especialitats

    usage::

        >>> import queries
        >>> spec_name = get_Spec_Name(19)
        >>> print(spec_name)

    :param:
    :rtype: string
"""
def get_Spec_Name(p_idSpec):
    try:
        res = ''
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('select f_nomEspecialitat from dm_especialitats where f_idEspecialitat = ' + str(p_idSpec))
            rows = cursor.fetchall()
            for result in rows:
                res = result[0]
            return res

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Retrieves the agenda name from table dm_especialitat_agenda

    usage::

        >>> import queries
        >>> agenda_name = get_Agenda_Name('19')
        >>> print(agenda_name)

    :param:
    :rtype: string
"""
def get_Agenda_Name(p_idAgenda):
    try:
        res = ''
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('select f_nomAgenda from dm_especialitat_agenda where f_idAgenda = \'' + p_idAgenda + '\'')
            rows = cursor.fetchall()
            for result in rows:
                res = result[0]
            return res

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Generates an array of all years in table dm2_stats_per_month in format YYYY.

    usage::

        >>> import queries
        >>> year_array = get_Years()
        >>> for year in year_array:
        >>>     print(year.year)

    :param:
    :rtype: array of tuples {'year': year}
"""
def get_Years():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT distinct LEFT(f_month, 4) from dm2_stats_per_month ORDER BY LEFT(f_month, 4) ASC'
            )
            rows = cursor.fetchall()
            lines = []
            line = {}
            for result in rows:
                line = {'year': result[0]}
                lines.append(line)
                line = {}
            return lines

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" Counts the number of visits and diferent patients in a time range.
    Can be uses with no range to calculate totals

    usage::

        >>> import queries
        >>> #whole 2018
        >>> visits, patients = get_Visits(2018)
        >>> #2018 till march
        >>> visits, patients = get_Visits(2018, 201803)
        >>> #whole stats
        >>> visits, patients = get_Visits()


    :param:
    :rtype: tuple visits,patients
"""
def get_Visits(p_year=None, p_lastmonth=None):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'SELECT COUNT(*) as visites, COUNT(distinct numHistoria) as pacients FROM bi_visites'
            if p_year is not None:
                if p_lastmonth is None:
                    sql = sql + ' WHERE LEFT(dataProgramacio, 4) = \'' + p_year + '\''
                else:
                    sql = sql + ' WHERE LEFT(dataProgramacio, 4) = \'' + p_year + '\' AND REPLACE(LEFT(dataProgramacio,7),"-","") <= \'' + p_lastmonth + '\''

            cursor.execute(sql)
            rows = cursor.fetchall()

            return rows[0][0], rows[0][1]

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" For each agenda in dm1_visits_per_agenda, counts the number of visits of
    given month (format YYYYMM), visits of the same month of last year and
    interanual variation in %. Comparative to previous month is also given.

    usage::

        >>> import queries
        >>> agendas_array = get_KPI_Agendas(201904)
        >>> for agenda in agendas_array:
        >>>     print(agenda.name + ': ' + agenda.inc + '%')


    :param:
    :rtype: array of tuples {'name': name, 'visites': visits, 'visitesUltimAny': visits12monthsago, 'inc': interanual_inc, 'visites_mes_anterior': visites_mes_anterior, 'inc_mensual': inc_mensual}
"""
def get_KPI_Agendas(p_lastmonth):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            previous_month = u.yyyymm_add_months(p_lastmonth, -1)
            sql = 'select va.f_nomAgenda, va.f_count, (select va3.f_count from dm1_visits_per_agenda va3 where va3.f_idAgenda = va.f_idAgenda and va3.f_month='+previous_month+') as f_count_previousMonth, (select va2.f_count from dm1_visits_per_agenda va2 where va2.f_idAgenda = va.f_idAgenda and va2.f_monthname=va.f_monthname and va2.f_year = (va.f_year-1)) as f_count_lastYear from dm1_visits_per_agenda va where va.f_month='+ p_lastmonth
            cursor.execute(sql)
            rows = cursor.fetchall()
            lines = []
            line = {}
            for result in rows:
                #calc interanual increment
                inc = 0
                visitesUltimAny = result[3]
                if result[3] is None:
                    visitesUltimAny = 0
                if not result[1] is None and visitesUltimAny != 0:
                    inc = int(round(100*result[1] / visitesUltimAny - 100.00, 2))
                #calc previous month increment
                inc_mensual = 0
                visites_mes_anterior = result[2]
                if result[2] is None:
                    visites_mes_anterior = 0
                if not result[1] is None and visites_mes_anterior != 0:
                    inc_mensual = int(round(100*result[1] / visites_mes_anterior - 100.00, 2))

                line = {'name': result[0],
                        'visites': result[1],
                        'visitesUltimAny': visitesUltimAny,
                        'inc': inc,
                        'visites_mes_anterior': visites_mes_anterior,
                        'inc_mensual': inc_mensual}
                lines.append(line)
                line = {}
            return lines

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()


""" For each agenda in dm1_visits_per_agenda, counts the number of visits of
    given month (format YYYYMM), visits of the same month of last year and
    interanual variation in %. Comparative to previous month is also given.

    usage::

        >>> import queries
        >>> agendas_array = get_KPI_Agendas(201904)
        >>> for agenda in agendas_array:
        >>>     print(agenda.name + ': ' + agenda.inc + '%')


    :param:
    :rtype: array of tuples {'name': name, 'visites': visits, 'visitesUltimAny': visits12monthsago, 'inc': interanual_inc, 'visites_mes_anterior': visites_mes_anterior, 'inc_mensual': inc_mensual}
"""
def get_KPI_general(p_num_months):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            # resulting dataframe will be transposed, so column order is important
            sql = 'SELECT f_month, f_visits_casuals+f_visits_fidelitzats as f_visits, f_patients,f_new_patients,f_casuals,f_fidelitzats,f_visits_casuals,f_visits_fidelitzats FROM datawarehouse.dm2_stats_per_month ORDER BY f_month DESC LIMIT '+str(p_num_months+1)
            df = pd.read_sql(sql, connection)
            df = df.sort_values(by=['f_month'])
            """
            dataframe has now as many rows as attributes we want to analise, and p_num_months+1 columns
            row 0: f_month (heading)
            row 1: f_visits
            row 2: f_patients
            row 3: f_new_patients
            row 4: f_casuals
            row 5: f_fidelitzats
            row 6: f_visits_casuals
            row 7: f_visits_fidelitzats
            """
            month = 0
            patients = 0
            new_patients = 0
            casual_patients = 0
            fidelizied_patients = 0
            visits_casual_patients = 0
            visits_fidelizied_patients = 0
            visits = 0

            matrix = np.zeros((p_num_months+1, 15))
            matrix = matrix.astype('str')
            matrix[0][0]=''
            matrix[0][1]='Pacients'
            matrix[0][2]='Captació'
            matrix[0][3]='Pacients casuals'
            matrix[0][4]='Pacients fidelitzats'
            matrix[0][5]='Visites casuals'
            matrix[0][6]='Visites fidelitzats'
            matrix[0][7]='inc_patients'
            matrix[0][8]='inc_new_patients'
            matrix[0][9]='inc_casual_patients'
            matrix[0][10]='inc_fidelizied_patients'
            matrix[0][11]='inc_visits_casual_patients'
            matrix[0][12]='inc_visits_fidelizied_patients'
            matrix[0][13]='Visites'
            matrix[0][14]='inc_visits'
            i = 1;
            for index, row in df.iterrows():
                if month == 0:
                    #we are in the extra row. we only need it to calc first row variation
                    month = row['f_month']
                    patients = row['f_patients']
                    new_patients = row['f_new_patients']
                    casual_patients = row['f_casuals']
                    fidelizied_patients = row['f_fidelitzats']
                    visits_casual_patients = row['f_visits_casuals']
                    visits_fidelizied_patients = row['f_visits_fidelitzats']
                    visits = row['f_visits']
                    continue
                #calc increments: current value - last value
                inc_patients = row['f_patients'] - patients
                inc_new_patients = row['f_new_patients'] - new_patients
                inc_casual_patients = row['f_casuals'] - casual_patients
                inc_fidelizied_patients = row['f_fidelitzats'] - fidelizied_patients
                inc_visits_casual_patients = row['f_visits_casuals'] - visits_casual_patients
                inc_visits_fidelizied_patients = row['f_visits_fidelitzats'] - visits_fidelizied_patients
                inc_visits = row['f_visits'] - visits

                month = row['f_month']
                patients = row['f_patients']
                new_patients = row['f_new_patients']
                casual_patients = row['f_casuals']
                fidelizied_patients = row['f_fidelitzats']
                visits_casual_patients = row['f_visits_casuals']
                visits_fidelizied_patients = row['f_visits_fidelitzats']
                visits = row['f_visits']
                matrix[i][0]=u.yyyymmToMonthName(str(month))
                matrix[i][1]=patients
                matrix[i][2]=new_patients
                matrix[i][3]=casual_patients
                matrix[i][4]=fidelizied_patients
                matrix[i][5]=visits_casual_patients
                matrix[i][6]=visits_fidelizied_patients
                matrix[i][7]=inc_patients
                matrix[i][8]=inc_new_patients
                matrix[i][9]=inc_casual_patients
                matrix[i][10]=inc_fidelizied_patients
                matrix[i][11]=inc_visits_casual_patients
                matrix[i][12]=inc_visits_fidelizied_patients
                matrix[i][13]=visits
                matrix[i][14]=inc_visits
                i += 1
            return np.transpose(matrix)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            connection.close()


""" Get the last number of load log lines.

    usage::

        >>> import queries
        >>> load_array = get_last_loads(5)
        >>> for load in load_array:
        >>>     print(load.load_date + ': ' + load.result + '%')


    :param:
    :rtype: array of tuples {'load_date': load_date, 'result': result}
"""
def get_last_loads(p_num_loads):
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'SELECT f_date as load_date, f_result as result FROM dm_load_log ORDER BY f_date DESC LIMIT ' + str(p_num_loads)
            cursor.execute(sql)
            rows = cursor.fetchall()
            lines = []
            line = {}
            for result in rows:
                line = {'load_date': result[0], 'result': result[1]}
                lines.append(line)
                line = {}
            return lines

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()
