import mysql.connector
import config
from mysql.connector import errorcode
import time
import datetime
import re
import xlrd

older_date = ''
older_date_aux = 0
newer_date = ''
newer_date_aux = 900000

gun_type_set = set()

#pip3 install mysql-connector-python

def do_add(s, x):
  l = len(s)
  s.add(x)
  return len(s) != l
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
CREATE TABLE IF NOT EXISTS `gun_violence`.`aux` (
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
book = xlrd.open_workbook('../dataset/gun-violence-data_01-2013_03-2018.xlsx')
sheet = book.sheet_by_index(0)
#book = xlrd.open_workbook('../dataset/teste.xlsx')
#sheet = book.sheet_by_index(0)

rows= sheet.nrows

i=0
print(f'Handling the dataset...')
for row in range(1,rows):
    
  #Some ids weren't numbers and the date needs to be a date
  if sheet.cell_type(row,0)==2  and sheet.cell_type(row,1)==3 and not(re.search("-[0-9].*",str(sheet.cell_value(row,17)))):
    incident_id = int(sheet.cell_value(row,0))
    date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row,1), book.datemode))

    #To get newer and oldest date
    diff = str(datetime.datetime.today()-date)
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
              
    state = sheet.cell_value(row,2)
    city_or_county = sheet.cell_value(row,3)
    if sheet.cell_type(row,4)==1:
      address = sheet.cell_value(row,4).replace('"','')
    else:
      address = ""
    n_killed = int(sheet.cell_value(row,5)) if sheet.cell_value(row,5) != "" else "NULL" 
    n_injured = int(sheet.cell_value(row,6)) if sheet.cell_value(row,6) != "" else "NULL"
    gun_stolen = sheet.cell_value(row,11)
    gun_type = sheet.cell_value(row,12)
    
    if sheet.cell_type(row,13)==1:
      incident_characteristics = sheet.cell_value(row,13).replace('"','')
    elif sheet.cell_type(row,13)==3:
      incident_characteristics = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row,13), book.datemode))
    else: 
      incident_characteristics = sheet.cell_value(row,13)

    latitude = sheet.cell_value(row,14) if sheet.cell_value(row,14) != "" else "NULL" 
    
    if sheet.cell_type(row,15)==1 and sheet.cell_type(row,15)!=3:
      location_description = sheet.cell_value(row,15).replace('"','')
    else: 
      location_description = sheet.cell_value(row,15)
    
    longitude = sheet.cell_value(row,16) if sheet.cell_value(row,16) != "" else "NULL"
    n_guns_involved = int(sheet.cell_value(row,17)) if sheet.cell_value(row,17) != "" else "NULL"
    
    if sheet.cell_type(row,18)==1:
      notes = sheet.cell_value(row,18).replace('"','')
    elif sheet.cell_type(row,18)==3:
      notes = ""
    else: 
      notes = sheet.cell_value(row,18)

    participant_age = sheet.cell_value(row,19)
    participant_age_group = sheet.cell_value(row,20)
    participant_gender = sheet.cell_value(row,21)
    participant_name = sheet.cell_value(row,22).replace('"','')
    participant_relationship = sheet.cell_value(row,23)
    participant_status = sheet.cell_value(row,24)
    participant_type = sheet.cell_value(row,25)
    state_house_district = int(sheet.cell_value(row,27)) if sheet.cell_type(row,27) == 2 else "NULL" 
    state_senate_district  = int(sheet.cell_value(row,28)) if sheet.cell_type(row,28) == 2 else "NULL" 

    if gun_type != "":
      if '||' in gun_type:
        splitted = gun_type.split("||")
        for gun in splitted:
          type = gun.split("::")[-1]
          gun_type_set.add(type)
      else:
        splitted = gun_type.split("|")
        for gun in splitted:
          type = gun.split(":")[-1]
          gun_type_set.add(type)

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

print(f'Total lines {rows}, meaningful lines {i}')

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


cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating dim_gun_stolen...")
cursor.execute("insert into dim_gun_stolen (dim_gun_stolen_id,class_stolen) VALUES (1,'Unknown');")
cursor.execute("insert into dim_gun_stolen (dim_gun_stolen_id,class_stolen) VALUES (2,'Stolen');")
cursor.execute("insert into dim_gun_stolen (dim_gun_stolen_id,class_stolen) VALUES (3,'Not-stolen');")
print("done")
cursor.close()

cnx.commit()


cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating dim_gun_type...")
x=1
for val in gun_type_set:
  cursor.execute(f'INSERT INTO gun_violence.dim_gun_type (dim_gun_type_id,class_type) VALUES ({x},"{val}");\n')
  x+=1

print("done")
cursor.close()

cnx.commit()
