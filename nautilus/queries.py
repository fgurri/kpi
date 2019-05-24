import mysql.connector
from mysql.connector import Error
import configparser

# read properties on project root
config = configparser.RawConfigParser()
config.read(r'nautilus.properties')


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


def get_Agendas():
    try:
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                'SELECT f_idAgenda, f_nomAgenda FROM datawarehouse.dm_especialitat_agenda ORDER BY f_nomAgenda ASC'
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


def get_Spec_Name(p_idSpec):
    try:
        res = ''
        connection = mysql.connector.connect(host=config.get('DatabaseSection', 'database.host'),
                                             database=config.get('DatabaseSection', 'database.dbname'),
                                             user=config.get('DatabaseSection', 'database.user'),
                                             password=config.get('DatabaseSection', 'database.password'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('select f_nomEspecialitat from dm_especialitats where f_idEspecialitat = ' + p_idSpec)
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
