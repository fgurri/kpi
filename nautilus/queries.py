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
