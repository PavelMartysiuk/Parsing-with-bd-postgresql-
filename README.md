#Parser data and news of coronavirus.


1) Script parses data and news of coronavitus in Russia from site  https://стопкоронавирус.рф//.
Script saves this data in database on Postgresql into two tables russia and news.

Table news is table for news from this site.

#Structure of table "news":

Column id is colunm for number of record.
Column title is colunm for title of news.
Column content is colunm for content.
Colunm source is column for link of source.
Column date is column for pubdate of news.

Table russia is table for statistic of rosonavirus in Russia.

#Strusture of table "russia":

Column id is colunm for number of record.
Column town is colunm for name of town.
Column sick is colunm for quantity of sicks.
Colunm recover is column for quantity of recovred.
Column death is column for quantity of deaths.
Column coordinates is column for coordinates of town.
Colimn date is column for date of parsing.

2) Script parses world statictic of coronavirus from site https://meduza.io/feature/2020/03/05/poslednie-dannye-po-koronavirusu-vo-vsem-mire-tablitsa.
Script saves this data in table world.

#Strurture of tables "world"
Column id is colunm for number of record.
Column country is colunm for name of country.
Column sick is colunm for quantity of sicks.
Colunm recover is column for quantity of recovred.
Column death is column for quantity of deaths.
Column coordinates is column for coordinates of town.
Colimn date is column for date of parsing.


#How use?
	First of the all should create database on Postgresql with name "Coronavirus"
	
	After this you should write this commands in cmd.
````
	pip install -r requirements.txt - this command installs all libaries.
	python tables - script creates tables in database "Coronavirus"
	python parse_coordinates - script creates json with coordinates of towns and countries.
	python parser - script creates records in batabase.
````
	
	
	


