import csv
import mysql.connector
import config
from mysql.connector import errorcode
import time
# try:
#     with open('../dataset/gun-violence-data_01-2013_03-2018.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         i=0
#         for row in reader:
#             incident_id = row['incident_id']
#             date = row['date']
#             state = row['state']
#             city_or_county = row['city_or_county']
#             address = row['address']
#             n_killed = row['n_killed']
#             n_injured = row['n_injured']
#             gun_stolen = row['gun_stolen']
#             gun_type = row['gun_type']
#             incident_characteristics = row['incident_characteristics']
#             latitude = row['latitude']
#             location_description = row['location_description']
#             longitude = row['longitude']
#             n_guns_involved = row['n_guns_involved']
#             notes = row['notes']
#             participant_age = row['participant_age']
#             participant_age_group = row['participant_age_group']
#             participant_gender = row['participant_gender']
#             participant_name = row['participant_name']
#             participant_relationship = row['participant_relationship']
#             participant_status = row['participant_status']
#             participant_type = row['participant_type']
#             state_house_district = row['state_house_district']
#             state_senate_district  = row['state_senate_district']
#             i+=1 
#         print(i)
# except Exception as e:
#     print(e)


try:
    cnx = mysql.connector.connect(user=config.user,
                                   password=config.password,
                                   host=config.host,
                                   database=config.database,
                                   auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
    cursor.execute("DROP PROCEDURE IF EXISTS gun.generate_Dates;")
    queryProc = """
    CREATE PROCEDURE gun.generate_Dates(date_start DATE, date_end DATE)
    BEGIN
	  WHILE date_start <= date_end DO
		  INSERT INTO gun.dim_date (date) VALUES (date_start);
		  SET date_start = date_add(date_start, INTERVAL 1 DAY);
	  END WHILE;
    END;"""
    cursor.execute(queryProc)
    query = "CALL gun.generate_Dates('2015-01-01','2020-11-30');" 
    cursor.execute(query)

    cnx.commit()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()


