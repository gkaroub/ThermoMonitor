import sqlite3
import os
import datetime

# Function definitions

# Sensors Db
def createSensorsDB(pathSensors): 
    conn = sqlite3.connect(pathSensors)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS TmLine")
    c.execute("""CREATE TABLE TmLine
        ( dtime DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
            tmpHOT REAL, 
            hmHOT REAL, 
            tmpCOLD REAL, 
            hmCOLD REAL);""")
    conn.commit()
    conn.close()

# Access DB
def createAccessDB(pathAccess):
    conn = sqlite3.connect(pathAccess)
    c = conn.cursor()
    c.execute("""CREATE TABLE access (id integer primary key autoincrement,
        name char(50), ibutton char(20));""")
    c.execute("""CREATE TABLE ins (id integer primary key autoincrement,
        access_id integer,allowed integer,dtime datetime default current_timestamp);""")
    c.execute("""CREATE VIEW entries2 as select access.name, CASE ins.allowed 
        WHEN 1 THEN 'NAI' ELSE 'OXI' END allowed, datetime(ins.dtime,'localtime') 
        from access, ins where access.id = ins.access_id  order by ins.dtime desc;""")
    c.execute("""CREATE VIEW entries1 as select access.name, CASE ins.allowed 
        WHEN 1 THEN 'NAI' ELSE 'OXI' END allowed, datetime(ins.dtime,'localtime')
        as dtime from access, ins where access.id = ins.access_id  order by ins.dtime desc;""")
    conn.commit()
    conn.close()

# Sensors DB creation
db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/sensorData.v2.db'

print("1. Sensors Database creation and initialization.")

if (os.path.isfile(db_abs_path)):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("The sensors database file exists. Do you want to overwrite? (y/n) ")
    if (answer == "y"):
        currentTime = str(datetime.datetime.now())
        currentTime = currentTime.replace(':', '_')
        currentTime = currentTime.replace(' ', '_')
        backFileName = '/sensorData.v2.db.bck.' + currentTime
        db_aps_path_backup = os.path.dirname(os.path.realpath(__file__)) + backFileName
        action = 'mv ' + db_abs_path + ' ' + db_aps_path_backup
        os.system(action)
        createSensorsDB(db_abs_path)
        print("Sensors Database is created and initialized.")
        print("The old db file is backed up!")
    else:
        print("Ok! Moving on to Access Control Database..")

if (os.path.isfile(db_abs_path) == False):
    #print(db_abs_path)
    createSensorsDB(db_abs_path)
    print("The sensors database file did not exist previously.")
    print("Sensors Database is created and initialized.")
    print("Ok! Moving on to Access Control Database.")

# Access DB Creation


db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/accessData.v2.db'

print("2. Access Control Database creation and initialization.")

if (os.path.isfile(db_abs_path)):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("The access control database file exists. Do you want to overwrite? (y/n) ")
    if (answer == "y"):
        currentTime = str(datetime.datetime.now())
        currentTime = currentTime.replace(':', '_')
        currentTime = currentTime.replace(' ', '_')
        backFileName = '/accessData.v2.db.bck.' + currentTime
        db_aps_path_backup = os.path.dirname(os.path.realpath(__file__)) + backFileName
        action = 'mv ' + db_abs_path + ' ' + db_aps_path_backup
        os.system(action)
        createAccessDB(db_abs_path)
        print("Access Control Database is created and initialized.")
        print("The old db file is backed up!")
    else:
        print("Ok! Bye")

if (os.path.isfile(db_abs_path) == False):
    #print(db_abs_path)
    createAccessDB(db_abs_path)
    print("The Access Control database file did not exist previously.")
    print("Access Control Database is created and initialized.")
    print("Ok! GoodBye.")
