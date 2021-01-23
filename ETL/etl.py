#!/usr/bin/python

import mysql.connector
import config
from mysql.connector import errorcode
import time
import datetime
import re
import xlrd
from functools import reduce 

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

def insert_dim_gun(cursor, stolen_gun, type_gun):
  cursor.execute(f'select dim_gun_type_id from gun_violence.dim_gun_type where class_type="{type_gun}";')
  id_gun_type, = cursor.fetchone()

  cursor.execute(f'select dim_gun_stolen_id from gun_violence.dim_gun_stolen where class_stolen="{stolen_gun}";')
  id_gun_stolen, = cursor.fetchone()
  
  cursor.execute(f'INSERT INTO gun_violence.dim_gun(facts_gun_incident_id,dim_gun_stolen_id,dim_gun_type_id) VALUES({incident_id},{id_gun_stolen},{id_gun_type});')

def to_dict(string, separator,scn_separator):
  ret = {}
  if string.strip() == "":
    return ret

  for e1 in string.split(separator):
    k,v = e1.split(scn_separator)
    ret[k] = v

  return ret


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
print(f'Loading the dataset...')
book = xlrd.open_workbook('../dataset/gun-violence-data_01-2013_03-2018.xlsx')
sheet = book.sheet_by_index(0)
#book = xlrd.open_workbook('../dataset/teste.xlsx')
#sheet = book.sheet_by_index(0)

rows= sheet.nrows
meaningful_lines=0
print(f'Handling the dataset...')
for row in range(1,rows):
    
  #Some ids weren't numbers and the date needs to be a date
  if sheet.cell_type(row,0)==2  and sheet.cell_type(row,1)==3 and not(re.search("-[0-9].*",str(sheet.cell_value(row,17)))) and not(re.search("District of Columbia",sheet.cell_value(row,2),re.IGNORECASE)):
    incident_id = int(sheet.cell_value(row,0))
    date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row,1), book.datemode))

    #To get newer and oldest date
    diff = str(datetime.datetime.today()-date)
    diff_days = int(diff.split(' ')[0])
    if meaningful_lines==0:
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

    address = sheet.cell_value(row,4).replace('"','') if sheet.cell_type(row,4)==1 else "N/A"
    n_killed = int(sheet.cell_value(row,5)) if sheet.cell_value(row,5) != "" else -1 
    n_injured = int(sheet.cell_value(row,6)) if sheet.cell_value(row,6) != "" else -1
    gun_stolen = sheet.cell_value(row,11)
    gun_type = sheet.cell_value(row,12)
    
    if sheet.cell_value(row,13)!="":
      if sheet.cell_type(row,13)==1:
        incident_characteristics = sheet.cell_value(row,13).replace('"','')
      elif sheet.cell_type(row,13)==3:
        x = re.search("00:00:00",str(xlrd.xldate_as_datetime(sheet.cell_value(row,13), book.datemode)))
        if x:
          incident_characteristics = (str(xlrd.xldate_as_datetime(sheet.cell_value(row,13), book.datemode)).split(" ")[0])
        else:
          incident_characteristics = (str(xlrd.xldate_as_datetime(sheet.cell_value(row,13), book.datemode)).split(" ")[-1])      
      else: 
        incident_characteristics = sheet.cell_value(row,13)
    else:
      incident_characteristics = "N/A" 
    
    latitude = sheet.cell_value(row,14) if sheet.cell_value(row,14) != "" else -1
    
    if sheet.cell_value(row,15)!="":
      location_description = sheet.cell_value(row,15).replace('"','') if sheet.cell_type(row,15)==1 and sheet.cell_type(row,15)!=3 else sheet.cell_value(row,15) 
    else:
      location_description = "N/A"
    longitude = sheet.cell_value(row,16) if sheet.cell_value(row,16) != "" else -1
    
    if sheet.cell_value(row,18)!="":
      if sheet.cell_type(row,18)==1:
        notes = sheet.cell_value(row,18).replace('"','')
      elif sheet.cell_type(row,18)==3:
        x = re.search("00:00:00",str(xlrd.xldate_as_datetime(sheet.cell_value(row,18), book.datemode)))
        if x:
          notes = (str(xlrd.xldate_as_datetime(sheet.cell_value(row,18), book.datemode)).split(" ")[0])
        else:
          notes = (str(xlrd.xldate_as_datetime(sheet.cell_value(row,18), book.datemode)).split(" ")[-1])      
      else: 
        notes = sheet.cell_value(row,18)
    else:
      notes = "N/A"  

    if sheet.cell_type(row,19) != 2:
      if sheet.cell_type(row,19) == 3:
        x = sheet.cell_value(row,19) # a float
        x = int(x * 24 * 3600) # convert to number of seconds
        participant_age = f'{x//3600}:{(x%3600)//60}' 
      else:
        participant_age = sheet.cell_value(row,19)

    participant_age_group = sheet.cell_value(row,20)
    participant_gender = sheet.cell_value(row,21)
    participant_name = sheet.cell_value(row,22).replace('"','')
    participant_relationship = sheet.cell_value(row,23)
    participant_status = sheet.cell_value(row,24)
    participant_type = sheet.cell_value(row,25)
    state_house_district = int(sheet.cell_value(row,27)) if sheet.cell_type(row,27) == 2 else -1 
    state_senate_district  = int(sheet.cell_value(row,28)) if sheet.cell_type(row,28) == 2 else -1 

    
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
      f'notes, participant_age,\n'
      f'participant_age_group, participant_gender,\n'
      f'participant_name, participant_relationship,\n'
      f'participant_status, participant_type,\n'
      f'state_house_district,state_senate_district) VALUES\n'
                
      f'("{incident_id}", "{date}", "{state}", "{city_or_county}", "{address}", {n_killed},\n'
      f'{n_injured}, "{gun_stolen}", "{gun_type}", "{incident_characteristics}",\n'
      f'{latitude}, "{location_description}", {longitude},\n'
      f'"{notes}", "{participant_age}",\n'
      f'"{participant_age_group}", "{participant_gender}",\n'
      f'"{participant_name}", "{participant_relationship}",\n'
      f'"{participant_status}", "{participant_type}",\n'
      f'{state_house_district}, {state_senate_district});'
    )
    meaningful_lines+=1

print(f'Total lines {rows}, meaningful lines {meaningful_lines}')

print(f'Older date: {older_date} | Newer date: {newer_date}')
print("---------------------------------------------")

print("Populating dim date...")
cursor.execute(f'CALL gun_violence.generate_Dates("{older_date}","{newer_date}");')
print("done")

print("---------------------------------------------")
print("Populating dim_participant_age_group...")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (1,'Adult 18+');")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (2,'Child 0-11');")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (3,'Teen 12-17');")
cursor.execute("insert into dim_participant_age_group (dim_participant_age_group_id,class_age_group) VALUES (4,'N/A');")
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
    INSERT INTO facts_gun_incident (incident_id, n_killed, n_injured, dim_date_id, dim_incident_info_id, dim_location_id)
    SELECT incident_id, n_killed, n_injured, t1.dim_date_id, incident_id, incident_id
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


cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating dim_gun...")
idAux=1
while idAux <= meaningful_lines:
  cursor.execute(f'select gun_stolen, gun_type, incident_id from gun_violence.aux where id={idAux}')
  gun = cursor.fetchone()
  gun_stolen, gun_type, incident_id = gun
  
  separator = "#"
  if gun_stolen != "" and gun_type != "" :
    if '||' in gun_type:
      separator = "||"
      scn_separator = "::"

    elif '|' in gun_type:
      separator= "|"
      scn_separator = ":"

    else:
      if '::' in gun_type:
        scn_separator = "::"
      else:
        scn_separator = ":"

    splitted_type = gun_type.split(separator)
    splitted_stolen = gun_stolen.split(separator)

    for i in range(len(splitted_type)):
      stolen_gun = splitted_stolen[i].split(scn_separator)[-1]
      type_gun = splitted_type[i].split(scn_separator)[-1]

      insert_dim_gun(cursor, stolen_gun, type_gun)

  idAux+=1
print("done")
cursor.close()

cnx.commit()


cursor=cnx.cursor()
print("---------------------------------------------")
print("Populating dim_participant...")
idAux=1
while idAux <= 20000:
  cursor.execute(f'select participant_gender, participant_name, participant_relationship, participant_status, participant_type, participant_age, participant_age_group from aux where id={idAux};')
  participants = cursor.fetchone()
  
  aux = tuple(filter(lambda x: len(x)>1,participants))
  
  selected = aux[0] if len(aux) > 0 else ""

  separator = ""
  
  if '||' in selected:
    separator = "||"
    scn_separator = "::"

  elif '|' in selected:
    separator= "|"
    scn_separator = ":"

  else:
    if '::' in selected:
      scn_separator = "::"
    else:
      scn_separator = ":"

  if separator != "":
    genders, names, relationships, statuss, types, ages, age_groups = tuple(map(lambda x: to_dict(x,separator,scn_separator),participants))
    max_len = reduce(lambda e1,e2: max(e1,len(e2.split(separator))),participants,0)
    
    for i in range(max_len):
      cursor.execute(f'select incident_id from aux where id={idAux};')
      incident_id, = cursor.fetchone()

      gender = genders[str(i)] if str(i) in genders else "N/A"
      name = names[str(i)] if str(i) in names else "N/A"
      relationship = relationships[str(i)] if str(i) in relationships else "N/A"
      status = statuss[str(i)] if str(i) in statuss else "N/A"
      ptype = types[str(i)] if str(i) in types else "N/A"
      age = ages[str(i)] if str(i) in ages else -1
      age_group = age_groups[str(i)] if str(i) in age_groups else "N/A"      

      # para buscar id age group
      if age_group != "N/A":
        cursor.execute(f'select dim_participant_age_group_id from dim_participant_age_group where class_age_group="{age_group}";')
        id_age_group, = cursor.fetchone()

      else:
        id_age_group = 4

      cursor.execute(f'INSERT INTO gun_violence.dim_participant (gender,name,relationship,status,type,dim_participant_age_group_id,age,facts_gun_incident_id) VALUES ("{gender}","{name}","{relationship}","{status}","{ptype}",{id_age_group},{age},{incident_id});')

  idAux+=1
print("done")
cursor.close()

cnx.commit()
