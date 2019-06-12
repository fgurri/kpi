import datetime
from django.test import TestCase, TransactionTestCase, Client
from django.db import connection, connections, transaction
import json

import nautilus.models as m
import nautilus.queries as q
import nautilus.utils as u
import nautilus.plots as p

def _run_sql_script(sql_script, cursor):
    f = open(sql_script, 'r')
    query = " ".join(f.readlines())
    cursor.execute(query)
"""
class TestUtils(TestCase):
    def setUp(self):
        self.empty_string = ''
        self.null_string = None
        self.yyyy_only = '2019'
        self.yyyymm_month_one_digit = '20198'
        self.yyyymmdd = '20190801'
        self.raw_date = datetime.datetime.now()
        self.not_numerical_string = 'ABCDEFG'
        self.valid_string = '201901'

    def test_yyyymmToMonthName(self):
        # bad formatted inputs should not raise an exception and return input
        self.assertTrue(self.empty_string == u.yyyymmToMonthName(self.empty_string))
        self.assertTrue(self.null_string == u.yyyymmToMonthName(self.null_string))
        self.assertTrue(self.yyyy_only == u.yyyymmToMonthName(self.yyyy_only))
        self.assertTrue(self.yyyymm_month_one_digit == u.yyyymmToMonthName(self.yyyymm_month_one_digit))
        self.assertTrue(self.yyyymmdd == u.yyyymmToMonthName(self.yyyymmdd))
        self.assertTrue(self.raw_date == u.yyyymmToMonthName(self.raw_date))
        self.assertTrue(self.not_numerical_string == u.yyyymmToMonthName(self.not_numerical_string))
        self.assertTrue('2019-Jan' == u.yyyymmToMonthName(self.valid_string))


    def test_yyyymm_add_months(self):
        self.assertTrue(self.empty_string == u.yyyymm_add_months(self.empty_string, 2))
        self.assertTrue(self.null_string == u.yyyymm_add_months(self.null_string, 5))
        self.assertTrue(self.yyyy_only == u.yyyymm_add_months(self.yyyy_only, -1))
        self.assertTrue(self.yyyymm_month_one_digit == u.yyyymm_add_months(self.yyyymm_month_one_digit, -3))
        self.assertTrue(self.yyyymmdd == u.yyyymm_add_months(self.yyyymmdd, 4))
        self.assertTrue(self.raw_date == u.yyyymm_add_months(self.raw_date, -1))
        self.assertTrue(self.not_numerical_string == u.yyyymm_add_months(self.not_numerical_string, 5))
        self.assertTrue(self.valid_string == u.yyyymm_add_months(self.valid_string, self.not_numerical_string))
        self.assertTrue('201810' == u.yyyymm_add_months(self.valid_string, -3))
        self.assertTrue('201905' == u.yyyymm_add_months(self.valid_string, 4))

class TestUrls(TransactionTestCase):
    databases = {'default', 'datawarehouse'}

    def setUp(self):
        # get cursor to datawarehouse db
        cursor = connections['datawarehouse'].cursor()
        # create tables in test db from script
        _run_sql_script('doc/create_tables.sql', cursor)

    def tearDown(self):
        # get cursor to datawarehouse db
        cursor = connections['datawarehouse'].cursor()
        # drop tables in test db from script
        _run_sql_script('doc/drop_tables.sql', cursor)

    def test_urls(self):
        c = Client()
        # existing urls
        self.assertTrue(c.post('/nautilus/').status_code == 200)
        self.assertTrue(c.post('/nautilus/dashboard').status_code == 200)
        self.assertTrue(c.post('/nautilus/pm').status_code == 200)
        self.assertTrue(c.post('/nautilus/papm').status_code == 200)
        self.assertTrue(c.post('/nautilus/pcpe').status_code == 200)
        self.assertTrue(c.post('/nautilus/nppe').status_code == 200)
        self.assertTrue(c.post('/nautilus/nptpe').status_code == 200)
        self.assertTrue(c.post('/nautilus/nppepm').status_code == 200)
        self.assertTrue(c.post('/nautilus/fbpa').status_code == 200)
        self.assertTrue(c.post('/nautilus/fbpaps').status_code == 200)
        self.assertTrue(c.post('/nautilus/fpa').status_code == 200)
        self.assertTrue(c.post('/nautilus/lvpm').status_code == 200)
        self.assertTrue(c.post('/nautilus/vpp').status_code == 200)
        self.assertTrue(c.post('/nautilus/pcpf').status_code == 200)
        self.assertTrue(c.post('/nautilus/dtlv').status_code == 200)
        self.assertTrue(c.post('/nautilus/info').status_code == 200)
        # not existing
        self.assertTrue(c.post('/dont_exists').status_code != 200)


class TestQueries(TransactionTestCase):
    databases = {'default', 'datawarehouse'}

    def setUp(self):
        # get cursor to datawarehouse db
        cursor = connections['datawarehouse'].cursor()
        # create tables in test db from script
        _run_sql_script('doc/create_tables.sql', cursor)
        # insert some test data
        sql_dm_especialitat_agenda = ("INSERT INTO dm_especialitat_agenda (f_idAgenda, f_idEspecialitat, f_nomAgenda) VALUES (%(f_idAgenda)s, %(f_idEspecialitat)s, %(f_nomAgenda)s)")
        json_dm_especialitat_agenda = json.load(open('test/dm_especialitat_agenda.json'))
        self.dm_especialitat_agenda_count = len(json_dm_especialitat_agenda)
        for row in json_dm_especialitat_agenda:
            cursor.execute(sql_dm_especialitat_agenda, row)

        sql_dm_especialitats = ("INSERT INTO dm_especialitats (f_idEspecialitat, f_nomEspecialitat) VALUES (%(f_idEspecialitat)s, %(f_nomEspecialitat)s)")
        json_dm_especialitats = json.load(open('test/dm_especialitats.json'))
        self.dm_especialitats_count = len(json_dm_especialitats)
        for row in json_dm_especialitats:
            cursor.execute(sql_dm_especialitats, row)

        sql_dm2_newpatient_per_month_agenda = ("INSERT INTO dm2_newpatient_per_month_agenda (`f_month`, `f_monthname`, `f_idAgenda`, `f_nomAgenda`, `f_idEspecialitat`, `f_nomEspecialitat`, `f_newPatients`) VALUES (%(f_month)s, %(f_monthname)s, %(f_idAgenda)s, %(f_nomAgenda)s, %(f_idEspecialitat)s, %(f_nomEspecialitat)s, %(f_newPatients)s);")
        json_dm2_newpatient_per_month_agenda = json.load(open('test/dm2_newpatient_per_month_agenda.json'))
        self.dm_dm2_newpatient_per_month_agenda_count = len(json_dm2_newpatient_per_month_agenda)
        for row in json_dm2_newpatient_per_month_agenda:
            cursor.execute(sql_dm2_newpatient_per_month_agenda, row)

    def tearDown(self):
        # get cursor to datawarehouse db
        cursor = connections['datawarehouse'].cursor()
        # drop tables in test db from script
        _run_sql_script('doc/drop_tables.sql', cursor)

    def test_get_agendas(self):
        agenda_list = q.get_Agendas()
        self.assertTrue(len(agenda_list) == self.dm_especialitat_agenda_count)

    def test_get_specialities(self):
        spec_list = q.get_Specialities()
        self.assertTrue(len(spec_list) == self.dm_especialitats_count)

    def test_get_Months(self):
        month_array = q.get_Months()
        month_list = q.get_month_list()
        # manually calc expected value from db
        cursor = connections['datawarehouse'].cursor()
        cursor.execute('SELECT COUNT(DISTINCT(f_month)) FROM dm2_newpatient_per_month_agenda')
        month_array_db = cursor.fetchone()[0]
        self.assertTrue(len(month_list) == month_array_db)
        self.assertTrue(len(month_array) == month_array_db)

    def test_get_agenda_name(self):
        cursor = connections['datawarehouse'].cursor()
        cursor.execute('SELECT f_idAgenda, f_nomAgenda FROM dm_especialitat_agenda')
        for row in cursor.fetchall():
            agenda_name = row[1]
            self.assertTrue(agenda_name == q.get_Agenda_Name(row[0]))

    def test_get_spec_name(self):
        cursor = connections['datawarehouse'].cursor()
        cursor.execute('SELECT f_idEspecialitat, f_nomEspecialitat FROM dm_especialitats')
        rows = cursor.fetchall()
        for row in rows:
            spec_name = row[1]
            self.assertTrue(spec_name == q.get_Spec_Name(row[0]))

    def test_get_Years(self):
        year_array = q.get_Years()
        # manually calc expected value from db
        cursor = connections['datawarehouse'].cursor()
        cursor.execute('SELECT COUNT(DISTINCT(LEFT(f_month,4))) FROM dm2_newpatient_per_month_agenda')
        year_array_db = cursor.fetchone()[0]
        self.assertTrue(len(year_array) == year_array_db)
"""

class TestPlots(TransactionTestCase):
    databases = {'default', 'datawarehouse'}

    def setUp(self):
        # get cursor to datawarehouse db
        cursor = connections['datawarehouse'].cursor()
        # create tables in test db from script
        _run_sql_script('doc/create_tables.sql', cursor)
        # insert some test data
        sql_dm2_stats_per_month = "INSERT INTO dm2_stats_per_month (`f_month`, `f_monthname`, `f_patients`, `f_new_patients`, `f_casuals`, `f_fidelitzats`, `f_visits_casuals`, `f_visits_fidelitzats`, `f_visits`, `f_inc_visits`, `f_inc_patients`, `f_inc_new_patients`, `f_inc_casuals`, `f_inc_fidelitzats`, `f_inc_visits_casuals`, `f_inc_visits_fidelitzats`) VALUES (%(f_month)s, %(f_monthname)s, %(f_patients)s, %(f_new_patients)s, %(f_casuals)s, %(f_fidelitzats)s, %(f_visits_casuals)s, %(f_visits_fidelitzats)s, %(f_visits)s, %(f_inc_visits)s, %(f_inc_patients)s, %(f_inc_new_patients)s, %(f_inc_casuals)s, %(f_inc_fidelitzats)s, %(f_inc_visits_casuals)s, %(f_inc_visits_fidelitzats)s)"
        json_dm2_stats_per_month = json.load(open('test/dm2_stats_per_month.json'))
        for row in json_dm2_stats_per_month:
            cursor.execute(sql_dm2_stats_per_month, row)

        sql_dm2_newpatient_per_month_agenda = ("INSERT INTO dm2_newpatient_per_month_agenda (`f_month`, `f_monthname`, `f_idAgenda`, `f_nomAgenda`, `f_idEspecialitat`, `f_nomEspecialitat`, `f_newPatients`) VALUES (%(f_month)s, %(f_monthname)s, %(f_idAgenda)s, %(f_nomAgenda)s, %(f_idEspecialitat)s, %(f_nomEspecialitat)s, %(f_newPatients)s);")
        json_dm2_newpatient_per_month_agenda = json.load(open('test/dm2_newpatient_per_month_agenda.json'))
        for row in json_dm2_newpatient_per_month_agenda:
            cursor.execute(sql_dm2_newpatient_per_month_agenda, row)

        sql_dm1_visits_per_agenda = ("INSERT INTO dm1_visits_per_agenda (`f_idAgenda`,`f_nomAgenda`,`f_idEspecialitat`,`f_nomEspecialitat`,`f_year`,`f_month`,`f_count`,`f_monthname`,`f_patients`) VALUES (%(f_idAgenda)s,%(f_nomAgenda)s,%(f_idEspecialitat)s,%(f_nomEspecialitat)s,%(f_year)s,%(f_month)s,%(f_count)s,%(f_monthname)s,%(f_patients)s);")
        json_dm1_visits_per_agenda = json.load(open('test/dm1_visits_per_agenda.json'))
        for row in json_dm1_visits_per_agenda:
            cursor.execute(sql_dm1_visits_per_agenda, row)

        sql_dm_first_visit = ("INSERT INTO dm_first_visit (`f_numHistoria`,`f_numPeticio`,`f_month`,`f_monthname`,`f_idAgenda`,`f_nomAgenda`,`f_idEspecialitat`,`f_nomEspecialitat`,`f_lastNumPeticio`,`f_lastmonth`,`f_lastmonthname`,`f_lastIdAgenda`,`f_lastNomAgenda`,`f_lastIdEspecialitat`,`f_lastNomEspecialitat`,`f_totalVisits`,`f_agendesDiferents`) VALUES (%(f_numHistoria)s,%(f_numPeticio)s,%(f_month)s,%(f_monthname)s,%(f_idAgenda)s,%(f_nomAgenda)s,%(f_idEspecialitat)s,%(f_nomEspecialitat)s,%(f_lastNumPeticio)s,%(f_lastmonth)s,%(f_lastmonthname)s,%(f_lastIdAgenda)s,%(f_lastNomAgenda)s,%(f_lastIdEspecialitat)s,%(f_lastNomEspecialitat)s,%(f_totalVisits)s,%(f_agendesDiferents)s);")
        json_dm_first_visit = json.load(open('test/dm_first_visit.json'))
        for row in json_dm_first_visit:
            cursor.execute(sql_dm_first_visit, row)


    def tearDown(self):
        # get cursor to datawarehouse db
        cursor = connections['datawarehouse'].cursor()
        # drop tables in test db from script
        _run_sql_script('doc/drop_tables.sql', cursor)


    def test_plot_patients_per_month(self):
        div = p.plot_patients_per_month()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_visits_per_month(self):
        div = p.plot_visits_per_month()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_distribution_visits_per_speciality(self):
        div = p.plot_distribution_visits_per_speciality('201501','201502')
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_visits_per_month_speciality(self):
        #by spec
        div = p.plot_visits_per_month_speciality(p_id_especiality=19)
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)
        #by agenda
        div = p.plot_visits_per_month_speciality(p_id_agenda='AG100')
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_frequency_per_agenda(self):
        div = p.plot_frequency_per_agenda('AG100')
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_patients_per_month(self):
        div = p.plot_patients_per_month()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_new_patients_per_month(self):
        div = p.plot_new_patients_per_month()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_distribution_new_patients(self):
        div = p.plot_distribution_new_patients()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_new_patients_per_speciality_per_month(self):
        div = p.plot_new_patients_per_speciality_per_month()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_evolution_new_patients_per_spec(self):
        #by spec
        div = p.plot_evolution_new_patients_per_spec(p_id_especiality=19)
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)
        #by agenda
        div = p.plot_evolution_new_patients_per_spec(p_id_agenda='AG100')
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_distribution_new_patients_per_spec(self):
        div = p.plot_distribution_new_patients_per_spec('201501','201502')
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_first_blood_per_agenda(self):
        div = p.plot_first_blood_per_agenda('201501','201502')
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

        div = p.plot_first_blood_per_agenda('201501','201502', 19)
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_last_visits_per_month(self):
        div = p.plot_last_visits_per_month()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)

    def test_plot_visits_per_patient(self):
        div = p.plot_visits_per_patient()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)


    def test_plot_distribution_casual_vs_fidelizied(self):
        div1, div2 = p.plot_distribution_casual_vs_fidelizied()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div1)
        self.assertIn("plotly-graph-div", div2)


    def test_plot_distance_to_lastmonth(self):
        div = p.plot_distance_to_lastmonth()
        # check if it generated a plotly div
        self.assertIn("plotly-graph-div", div)
