<h1>Summary</h1>
<p>Calculates some Key Performance Indicators (KPI's) from data warehouse pregenerated tables for a Healthcare company.</p>
<p>Examples of KPI's:
<li>Assistance evolution per agenda, speciality or month</li>
<li>New patients generation analysis</li>
<li>Visits generated per first visits in agenda</li>
<li>Months till last visit of each patient</li>
<li>Distribution of volumes casual vs fidelizied patients</li>
<li>Visits per patient</li>
<li>etc</li>
</p>


<h1>Folder content</h1>
<li>ETL: kettle data jobs scheduled to generate data warehouse tables</li>
<li>doc: sql files for table creation used in tests and in DB creation. File "requirements.txt" includes packages+version used in the app</li>
<li>kpi: core django project's app. File "settings.py" contains most configuration</li>
<li>nautilus: main app code</li>
<li>static: static project folder. There is an additional static folder inside nautilus app</li>
<li>test: json files containing test data</li>


<h1>Tools</h1>
<li>django 2.2</li>
<li>python 3.6.4 (64 bits)</li>
<li>bootstrap 3</li>
<li>plotly for data visualization</li>
<li>Pentaho Data Integration for ETL from master (InterSystems Cache, MySql) to Data Warehouse (kettle transformations included in ETL folder)</li>
<li>authentication to LDAP company server</li>
<li>See requirements.txt in doc folder for additional packages used</li>
