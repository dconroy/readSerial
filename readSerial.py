#!/usr/bin/env python

# Import the necessary shiz
import serial
import sys
import sqlite3
import time
import datetime
import requests
import dictionary
import os
import time
<<<<<<< HEAD
import logging

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("Starting script..")

# Define sensor id, SQLdict and flag as global variables
id = 0
flag = True
SQLdict = {}

# Select USB0 if radio is connected to first USB port on Pi
logging.debug("Opening serial port")
try:
    serialport = serial.Serial("/dev/ttyUSB0", 115200) # make sure baud rate is the same
    logging.info("Serial port open successfully")
except:
    logging.warning("Serial port open FAILED")
=======


# Define sensor id and flag as global variables
id = 0
flag = True

# Select USB0 if radio is connected to first USB port on Pi
serialport = serial.Serial("/dev/ttyUSB0", 115200) # make sure baud rate is the same
>>>>>>> origin/master

# Set location of sqlite db & table name
db = '/home/pi/serial_db.sqlite'
tn = 'SERIAL_DB'

<<<<<<< HEAD
=======

>>>>>>> origin/master
# Create SQLLite Database, may already exist, handle exception
def create_db():
    #tn = 'SERIAL_DB'    #table name
    nf1 = 'node_id'     #new field
    ft1 = 'INTEGER'     #field type
    nf2 = 'sensor_type'
    ft2 = 'TEXT'
    nf3 = 'sensor_value'
    ft3 = 'REAL'
    nf4 = 'timestamp'
    ft4 = 'INTEGER'

    logging.debug("Connecting to database")
    conn = sqlite3.connect(db) #connect to db
    c = conn.cursor()

    logging.debug("Creating table/updating values")
    try:
        c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1}, {nf2} {ft2}, {nf3} {ft3}, {nf4} {ft4}, PRIMARY KEY({nf1},{nf2}))".format(tn=tn, nf1=nf1, ft1=ft1, nf2=nf2, ft2=ft2, nf3=nf3, ft3=ft3, nf4=nf4, ft4=ft4))
    except:
        logging.error("SQL command error")

    conn.commit()   #commit changes to db
    conn.close()    #close connection


# Read Serial port
def read_serial():
    logging.debug("Flushing serial I/O")
    serialport.flushInput() #clear input serial buffer
    serialport.flushOutput() #clear output serial buffer
    while True: # keep reading serial port and write to file till the end of time
        logging.debug("Waiting for serial data ...")
        #print("\nWaiting for serial data ...")
        data = serialport.readline() #expecting this format -> "i:1,t:25.44,h:40.23,l:34.00\n"
        logging.info("Data received via serial")
        #print data
        if data[0]=='i': # check if data is not empty and entire string is being sent (first value is always "i", which is node ID)
            final_data = parse(data) # parse data
            write_db(final_data)    # write data to SQLite db
            restAPI(final_data) # push data to HA via rest API
            checkFlag(final_data) # check if flag is False, then edit YAML files & restart HA
<<<<<<< HEAD
        else:
            logging.warning("Incomplete data packet received")
=======
            print("\nWaiting for serial data ...")
>>>>>>> origin/master

# Parse data string
def parse(data):
    final_data = {}
    for p in data.strip().split(","): #strip() removes trailing \n
        k,v = p.split(":")
        final_data[k] = v if v else 0.00
<<<<<<< HEAD
    logging.debug("Data parsed into dictionary")
    #print ("Final Data:")
    #print (final_data)
=======
    print ("Final Data:")
    print (final_data)
>>>>>>> origin/master
    return final_data


# Write data to SQLiteDB
def write_db(final_data): # one row per node, per sensor value, overwrite existing value
    global id # define again so glabal copy of id is also set
    global flag

    conn = sqlite3.connect(db) #connect to db
    c = conn.cursor()

    ts = int(time.time()) #get epoch time in seconds
    id = final_data.pop("i") #get sensor id
<<<<<<< HEAD
    #id = 172
=======
    #id = 156
>>>>>>> origin/master
    #st = sensor type, sv = sensor value
    logging.debug("Looking for data in SQLite DB")
    for k,v in final_data.iteritems():
        # check if data exists by checking node ID and sensor type
        a = "SELECT * FROM {tn} WHERE {nodeid} = '{id}' AND {stype}='{st}'".format(sv='sensor_value', stype='sensor_type', st=k, tn=tn, nodeid='node_id', id=id)
<<<<<<< HEAD
        #print(a)
        logging.debug(a)
        try:
            c.execute(a)
        except:
            logging.error("SQL command Error")
        data = c.fetchone() #returns one matching row; fetchall() returns all matching rows
        if not data:
            flag = False
            logging.debug("Node doesn't exist in DB")

        st = "INSERT OR REPLACE INTO {tn} VALUES ({id},'{st}', '{sv}', {ts})".format(id=id, tn=tn, st=k, sv=v, ts=ts)
        #print st
        logging.debug(st)
        logging.debug("Writing data to SQLite DB")
        try:
            c.execute(st)
        except:
            logging.error("SQL command Error")
=======
        print(a)
        c.execute(a)
        data = c.fetchone() #returns one matching row; fetchall() returns all matching rows
        if not data:
            flag = False

        st = "INSERT OR REPLACE INTO {tn} VALUES ({id},'{st}', {sv}, {ts})".format(id=id, tn=tn, st=k, sv=v, ts=ts)
        print st
        c.execute(st)
>>>>>>> origin/master

    conn.commit()   #commit changes to db
    conn.close() #close connection to SQL file after writing to it


# Publish data to HA via restAPI
def restAPI(final_data):
<<<<<<< HEAD
    global id # use global id instead of local
    for k,v in final_data.iteritems():
        if k == '#': continue # skip group name
        #id = final_data.pop("i") #get sensor id
        st = dictionary.sensorType[k]
        su = dictionary.sensorUnit[k]
        si = dictionary.sensorIcon[k]
        sn = dictionary.sensorName[k]

        url = 'http://127.0.0.1:8123/api/states/sensor.%s_%s' % (st, id)
        headers = {'x-ha-access': 'Abudabu1!',
                'content-type': 'application/json'}

        data  = '{"state" : "%s", "attributes": {"friendly_name": "%s", "unit_of_measurement": "%s", "icon": "%s"}}' % (v, sn, su, si)
=======
    for k,v in final_data.iteritems():
        #id = final_data.pop("i") #get sensor id
        st = dictionary.sensorType[k]
        su = dictionary.sensorUnit[k]

        url = 'http://192.168.1.212:8123/api/states/sensor.%s_%s' % (st, id)
        headers = {'x-ha-access': 'Abudabu1!',
                'content-type': 'application/json'}

        data  = '{"state" : "%s", "attributes": {"friendly_name": "%s", "unit_of_measurement": "%s"}}' % (v, st, su)
>>>>>>> origin/master

        req = requests.Request('POST', url, headers=headers, data=data)
        prepared = req.prepare()
        pretty_print_POST(prepared)

        #response = requests.post(url, headers=headers, data=data)
        #print(response.text)
<<<<<<< HEAD
        logging.debug("Sending data via REST API")
        #print("\nSending data via REST API\n")
        s = requests.Session()
        response = s.send(prepared)
        logging.debug(response)
=======
        print("\nSending data via REST API\n")
        s = requests.Session()
        s.send(prepared)
>>>>>>> origin/master


# Print POST request in a pretty way
def pretty_print_POST(req):
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


<<<<<<< HEAD
# Rewrite sensors YAML file with new info
def edit_sensors_YAML(final_data):
    global id # use global id instead of local
    filename = 'sensors.yaml'
    logging.debug("Editing %s" % (filename,))
    try:
        target = open('/home/pi/.homeassistant/%s' % (filename,), 'w') #open file in write mode
    except:
        logging.error("Error opening %s" % (filename,))

    target.truncate() # clear file
    target.write("#Sensors\n")

    for k,v in final_data.iteritems():
        if k == '#': continue # skip group name
        st = dictionary.sensorType[k]
        su = dictionary.sensorUnit[k]
        YAMLstring = "- platform: command_line\n  name: %s_%s\n  command: \"python /home/pi/readDb.py %s %s\"\n  unit_of_measurement: '%s'\n" % (st, id, k, id, su)
=======
# Rewrite custom sensors YAML file with new info
def edit_customsensors_YAML(final_data):
    target = open('/home/pi/.homeassistant/custom_sensors.yaml', 'w') #open file in write mode
    target.truncate() # clear file
    target.write("#Custom sensors\n")

    for k,v in final_data.iteritems():
        st = dictionary.sensorType[k]
        su = dictionary.sensorUnit[k]
        YAMLstring = "- platform: customsensor\n  name: %s %s\n  unit_of_measurement: '%s'\n" % (st, id, su)
>>>>>>> origin/master
        target.write(YAMLstring)

    target.write("\n")
    target.close() # important - close file

<<<<<<< HEAD
    logging.debug("%s edited" % (filename,))
    #print("Adding new sensor to HA")
    #print("sensors.yaml edited")


# Rewrite groups YAML file with new info
def edit_groups_YAML(final_data):
    global id # use global id instead of local
    filename = 'groups.yaml'
    logging.debug("Editing %s" % (filename,))
    try:
        target = open('/home/pi/.homeassistant/%s' % (filename,), 'w') #open file in write mode
    except:
        logging.error("Error opening %s" % (filename,))

    target.truncate() # clear file
    target.write("#Groups\n")
    target.write("Group {id}:\n  entities:\n".format(id=id))

    for k,v in final_data.iteritems():
        if k == '#': continue # skip group name
=======
    print("Adding new sensor to HA")
    print("custom_sensors.yaml edited")


# Rewrite custom groups YAML file with new info
def edit_customgroups_YAML(final_data):
    target = open('/home/pi/.homeassistant/custom_groups.yaml', 'w') #open file in write mode
    target.truncate() # clear file
    target.write("#Custom groups\n")
    target.write("Group {id}:\n  entities:\n".format(id=id))

    for k,v in final_data.iteritems():
>>>>>>> origin/master
        st = dictionary.sensorType[k]
        su = dictionary.sensorUnit[k]
        YAMLstring = "    - sensor.%s_%s\n" % (st, id)
        target.write(YAMLstring)

<<<<<<< HEAD
    gn = final_data.get('#', "Group {id}".format(id=id))    # get group name if exists

    target.write("    - script.export_{id}\n".format(id=id))
    target.write("    - weblink.download_csv_file\n")
    target.write("  name: {gn}\n".format(gn=gn))
    target.write("\n")
    target.close() # important - close file

    logging.debug("%s edited" % (filename,))
    #print("Adding new groups to HA")
    #print("groups.yaml edited")


# Rewrite customize YAML file with new info
def edit_customize_YAML(final_data):
    global id # use global id instead of local
    filename = 'customize.yaml'
    logging.debug("Editing %s" % (filename,))
    try:
        target = open('/home/pi/.homeassistant/%s' % (filename,), 'w') #open file in write mode
    except:
        logging.error("Error opening %s" % (filename,))

    target.truncate() # clear file
    target.write("#Customize nodes\n")

    for k,v in final_data.iteritems():
        if k == '#': continue # skip group name
=======
    target.write("  name: Group {id}\n".format(id=id))

    target.write("\n")
    target.close() # important - close file

    print("Adding new groups to HA")
    print("custom_groups.yaml edited")


# Rewrite custom customize YAML file with new info
def edit_customcustomize_YAML(final_data):
    target = open('/home/pi/.homeassistant/custom_customize.yaml', 'w') #open file in write mode
    target.truncate() # clear file
    target.write("#Customize custom nodes\n")

    for k,v in final_data.iteritems():
>>>>>>> origin/master
        st = dictionary.sensorType[k]
        su = dictionary.sensorUnit[k]
        si = dictionary.sensorIcon[k]
        sn = dictionary.sensorName[k]
        YAMLstring = "sensor.%s_%s:\n  friendly_name: %s\n  icon: %s\n" % (st, id, sn, si)
        target.write(YAMLstring)

<<<<<<< HEAD
    target.write("script.export_{id}:\n  icon: mdi:export\n".format(id=id))
    target.write("\n")
    target.close() # important - close file

    logging.debug("%s edited" % (filename,))
    #print("Customizing new nodes")
    #print("customize.yaml edited")


#Rewrite shell_commands YAML file with new info
def edit_shell_commands_YAML(final_data):
    global id # use global id instead of local
    filename = 'shell_commands.yaml'
    logging.debug("Editing %s" % (filename,))
    try:
        target = open('/home/pi/.homeassistant/%s' % (filename,), 'w') #open file in write mode
    except:
        logging.error("Error opening %s" % (filename,))

    target.truncate() # clear file
    target.write("#Shell commands\n")

    YAMLstring = "export_%s: python /home/pi/exportDb.py %s\n" % (id, id)
    target.write(YAMLstring)

    target.write("\n")
    target.close() # important - close file

    logging.debug("%s edited" % (filename,))
    #print("Adding export shell command")
    #print("shell_commands.yaml edited")


#Rewrite scripts YAML file with new info
def edit_scripts_YAML(final_data):
    global id # use global id instead of local
    filename = 'scripts.yaml'
    logging.debug("Editing %s" % (filename,))
    try:
        target = open('/home/pi/.homeassistant/%s' % (filename,), 'w') #open file in write mode
    except:
        logging.error("Error opening %s" % (filename,))

    target.truncate() # clear file
    target.write("#Scripts\n")

    YAMLstring = "export_%s:\n  alias: Export Data\n  sequence:\n    - service: shell_command.export_%s\n" % (id, id)
    target.write(YAMLstring)

    target.write("\n")
    target.close() # important - close file

    logging.debug("%s edited" % (filename,))
    #print("Adding export script")
    #print("scripts.yaml edited")

# create a dictionary of all node ids and sensor types
def create_SQL_dict():
    global SQLdict # use global variable

    logging.debug("Connecting to database")
    conn = sqlite3.connect(db) #connect to db
    c = conn.cursor()

    logging.debug("Creating dictionary of lists from database")
    try:
        c.execute("SELECT DISTINCT node_id FROM {tn}".format(tn=tn))
        ids = c.fetchall()
    except:
        logging.error("SQL command error")

    for i in ids:
        SQLdict[i[0]] = []
        try:
            c.execute("SELECT DISTINCT sensor_type FROM {tn} WHERE {nodeid} = {id}".format(nodeid='node_id',tn=tn, id=i[0]))
        except:
            logging.error("SQL command error")
        types = c.fetchall()
        SQLdict[i[0]] = [v[0] for v in types if v[0] != '#']

    logging.debug("Dictionary of lists created")
    conn.commit()   #commit changes to db
    conn.close()    #close connection
=======
    target.write("\n")
    target.close() # important - close file

    print("Adding new groups to HA")
    print("custom_customize.yaml edited")
>>>>>>> origin/master


# Check if flag is false, then edit YAML files & restart HA
def checkFlag(final_data):
    global flag
    if not flag:
<<<<<<< HEAD
        logging.debug("New node detected")
        #print("New node detected")
        create_SQL_dict()
        edit_sensors_YAML(final_data)
        edit_groups_YAML(final_data)
        edit_customize_YAML(final_data)
        edit_scripts_YAML(final_data)
        edit_shell_commands_YAML(final_data)
        flag = True  # set flag as true
        logging.info("Restarting Pi ...")
        #print("Restarting Pi ...")
        #os.system('sudo reboot')  # restart Pi
        #os.system('sudo systemctl restart home-assistant@pi') # very important - restart home assistant after editing config files

        #for i in range(5,0,-1):
        #    time.sleep(1)
        #    sys.stdout.write(str(i)+' ')
        #    sys.stdout.flush()
        #time.sleep(15) # delay for 15 seconds till HA is properly restarted

        os.system('sudo reboot')  # restart Pi

=======
        print("New node detected")
        edit_customsensors_YAML(final_data)
        edit_customgroups_YAML(final_data)
        edit_customcustomize_YAML(final_data)
        flag = True  # set flag as true
        print("Restarting Home Assistant ...")
        os.system('sudo systemctl restart home-assistant@pi') # very important - restart home assistant after editing config files
        for i in range(10,0,-1):
            time.sleep(1)
            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
        #time.sleep(15) # delay for 15 seconds till HA is properly restarted

>>>>>>> origin/master

#run
create_db()
read_serial()