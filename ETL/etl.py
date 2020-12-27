import csv
import mysql.connector
import config
from mysql.connector import errorcode
import time
import datetime
import re

older_date = ''
older_date_aux = 0
newer_date = ''
newer_date_aux = 900000


#apagar schema se ja tiver e criar atraves do create.sql
try:
    cnx = mysql.connector.connect(user=config.user,
                                   password=config.password,
                                   host=config.host,
                                   auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    cursor.execute("DROP SCHEMA IF EXISTS gun_violence;")
    print("Dropped schema gun_violence if existed")
    
    cnx._open_connection()
    
    print("---------------------------------------------")

    print("Creating gun_violence schema")
    with open('create.sql', 'r') as f:
      cursor.execute(f.read(), multi=True)
    print("gun_violence created")
    
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  else:
    print(err)
else:
  cnx.close()

print("---------------------------------------------")

#popular gun_violence
cnx = mysql.connector.connect(user=config.user,
                                   password=config.password,
                                   host=config.host,
                                   database=config.database,
                                   auth_plugin='mysql_native_password')
cursor = cnx.cursor()
cursor.execute("DROP PROCEDURE IF EXISTS gun_violence.generate_Dates;")
queryProc = """
    CREATE PROCEDURE gun_violence.generate_Dates(date_start DATE, date_end DATE)
    BEGIN
	  WHILE date_start <= date_end DO
		  INSERT INTO gun_violence.dim_date (date, day, month,year) VALUES (date_start,day(date_start),month(date_start),year(date_start));
		  SET date_start = date_add(date_start, INTERVAL 1 DAY);
	  END WHILE;
    END;"""
cursor.execute(queryProc)

cursor.execute("""
CREATE TEMPORARY TABLE IF NOT EXISTS `gun_violence`.`aux` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `incident_id` INT NULL,
  `date` DATE NULL,
  `state` TEXT NULL,
  `city_or_county` TEXT NULL,
  `address` TEXT NULL,
  `n_killed` INT NULL,
  `n_injured` INT NULL,
  `gun_stolen` TEXT NULL,
  `gun_type` TEXT NULL,
  `incident_characteristics` TEXT NULL,
  `latitude` DECIMAL(13,8) NULL,
  `location_description` TEXT NULL,
  `longitude` TEXT NULL,
  `n_guns_involved` INT NULL,
  `notes` TEXT NULL,
  `participant_age` TEXT NULL,
  `participant_age_group` TEXT NULL,
  `participant_gender` TEXT NULL,
  `participant_name` TEXT NULL,
  `participant_relationship` TEXT NULL,
  `participant_status` TEXT NULL,
  `participant_type` TEXT NULL,
  `state_house_district` INT NULL,
  `state_senate_district` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
""")


  


#tratar do dataset
try:
    with open('../dataset/gun-violence-data_01-2013_03-2018.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i=0
        j=0
        print(f'Handling the dataset...')
        for row in reader:
          #Some ids weren't numbers and the date needs to be a date
          if re.search("[0-9]+",row['incident_id']) and re.search("[0-9]+-[0-9]+-[0-9][1-9]",row['date']):
            incident_id = row['incident_id']
            date = row['date']
            #To get newer and oldest date
            diff = str(datetime.datetime.today()-datetime.datetime.strptime(date, '%Y-%m-%d'))
            diff_days = int(diff.split(' ')[0])
            if i==0:
              older_date=date
              older_date_aux = diff_days
              newer_date=date
              newer_date_aux = diff_days
            else:
              if diff_days > older_date_aux:
                older_date_aux = diff_days
                older_date=date
              if diff_days < newer_date_aux:
                newer_date=date
                newer_date_aux = diff_days
            
            state = row['state']
            city_or_county = row['city_or_county']
            address = row['address'].replace('"','')
            n_killed = int(row['n_killed']) if row['n_killed'] != "" else "NULL" 
            n_injured = int(row['n_injured']) if row['n_injured'] != "" else "NULL"
            gun_stolen = row['gun_stolen']
            gun_type = row['gun_type']
            incident_characteristics = row['incident_characteristics']
            latitude = float(row['latitude']) if row['latitude'] != "" else "NULL" 
            location_description = row['location_description'].replace('"','')
            longitude = float(row['longitude']) if row['longitude'] != "" else "NULL"
            n_guns_involved = int(row['n_guns_involved']) if row['n_guns_involved'] != "" else "NULL"
            notes = row['notes'].replace('"','')
            participant_age = row['participant_age']
            participant_age_group = row['participant_age_group']
            participant_gender = row['participant_gender']
            participant_name = row['participant_name'].replace('"','')
            participant_relationship = row['participant_relationship']
            participant_status = row['participant_status']
            participant_type = row['participant_type']
            state_house_district = int(row['state_house_district']) if row['state_house_district'] != "" else "NULL" 
            state_senate_district  = int(row['state_senate_district']) if row['state_senate_district'] != "" else "NULL" 

            cursor.execute(f' INSERT INTO gun_violence.aux (\n'
              f'incident_id, date, state, city_or_county, address, n_killed,\n'
              f'n_injured, gun_stolen, gun_type, incident_characteristics,\n'
              f'latitude, location_description, longitude,\n'
              f'n_guns_involved, notes, participant_age,\n'
              f'participant_age_group, participant_gender,\n'
              f'participant_name, participant_relationship,\n'
              f'participant_status, participant_type,\n'
              f'state_house_district,state_senate_district) VALUES\n'
              
              f'("{incident_id}", "{date}", "{state}", "{city_or_county}", "{address}", {n_killed},\n'
              f'{n_injured}, "{gun_stolen}", "{gun_type}", "{incident_characteristics}",\n'
              f'{latitude}, "{location_description}", {longitude},\n'
              f'{n_guns_involved}, "{notes}", "{participant_age}",\n'
              f'"{participant_age_group}", "{participant_gender}",\n'
              f'"{participant_name}", "{participant_relationship}",\n'
              f'"{participant_status}", "{participant_type}",\n'
              f'{state_house_district}, {state_senate_district});'
            )
            i+=1
          j+=1
        print(f'Total lines {j}, meaningful lines {i}')
except Exception as e:
    print(f'Hello -> {e}')

print(f'Older date: {older_date} | Newer date: {newer_date}')
print("---------------------------------------------")

print("Populating dim date...")
cursor.execute(f'CALL gun_violence.generate_Dates("{older_date}","{newer_date}");')
print("done")

print("---------------------------------------------")
print("Populating dim_participant_age_group...")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (1,'Adult 18+');")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (2,'Child 0-11');")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (3,'Teen 12-18');")
print("done")

print("---------------------------------------------")
print("Populating dim_state_district...")
cursor.execute("""
    INSERT INTO gun_violence.dim_state_district (dim_state_district_id,senate,house)
    SELECT incident_id,state_senate_district, state_house_district
    FROM gun_violence.aux
""")
print("done")

cursor.close()
cnx.commit()

cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating dim_incident_info...")
cursor.execute("""
  INSERT INTO gun_violence.dim_incident_info (dim_incident_info_id,incident_characteristics,notes)
  SELECT incident_id,incident_characteristics, notes
  FROM gun_violence.aux
  """)
print("done")
cursor.close()

cnx.commit()


cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating dim_location...")
cursor.execute("""
    INSERT INTO gun_violence.dim_location (dim_location_id,city_or_county,state,latitude,longitude,address,location_description,dim_state_district_id)
    SELECT incident_id,city_or_county,state,latitude,longitude,address,location_description,incident_id
    FROM gun_violence.aux
""")
print("done")
cursor.close()


cnx.commit()

cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating facts_gun_incident...")
cursor.execute("""
    INSERT INTO facts_gun_incident (incident_id, n_killed, n_injured, n_guns_involved, dim_date_id, dim_incident_info_id, dim_location_id)
    SELECT incident_id, n_killed, n_injured, n_guns_involved, t1.dim_date_id, incident_id, incident_id
    FROM gun_violence.aux t
    LEFT JOIN dim_date t1
    ON t.date=t1.date
""")
print("done")
cursor.close()


cnx.commit()
