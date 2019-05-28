#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error
 

__author__ = "ibanez.j@gmail.com"
__date__ = "July 4, 2017"
__license__ = "MIT"

from TwitterAPI import TwitterAPI, __version__
#from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterOAuth import TwitterOAuth

from os.path import expanduser




 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 

def insertNewSensors(conn):
    """
    """
    cur = conn.cursor()
    cur.execute("""
    insert into sensor_state (sensorId)
    SELECT hits.sensorId
    from sensor_hits as hits
    WHERE NOT EXISTS(SELECT 1 FROM sensor_state as state WHERE hits.sensorId = state.sensorId);
    """)
 
    #rows = cur.fetchall()
 
    #for row in rows:
    #    print(row)


def select_hits(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    cur = conn.cursor()
    cur.execute("""
    select  
            state.sensorId as id, hits.sensorId as hitsId,
            hits.counter as hits, state.stateName as state, 
            state.stateCounter as stateCounter,
            state.alias as alias
    from 
            sensor_state as state
    left join 
            sensor_hits as hits on hits.sensorId = state.sensorId;    
    """)

    rows = cur.fetchall()
 
    ret = []
    col_name_list = [tuple[0] for tuple in cur.description]
    #print col_name_list

    for row in rows:
        retRow = {}
        for idx, col in enumerate(row):
            retRow[col_name_list[idx]]=col
        #print retRow
        ret.append(retRow)

    #print ret
    return ret

 
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    rows = cur.fetchall()
 
    for row in rows:
        print(row)




def checkHits(hitsTable):

    for sensor in hitsTable:

        stateCounter = 0
        newState = "UNKN"

        #print sensor

        if sensor['hits'] > 0 :
            newState = "OK"

        elif sensor['state'] == 'OK':
            newState   = "PRE-ALARM"

        elif sensor['state'] == 'PRE-ALARM':
            newState   = "ALARM"

        elif sensor['state'] == 'ALARM' and int(sensor['stateCounter']) > 1:
            newState   = "DOWN"

        elif sensor['state'] == 'ALARM':
            newState   = "ALARM"
            stateCounter = int(sensor['stateCounter'])+1

        else:
            newState  = "DOWN"    

        sensor['newState']=newState
        sensor['newStateCounter'] = stateCounter

        print sensor

    #print hitsTable
    return hitsTable



def updateSensorStateTable(conn,hitsTable):

    for sensor in hitsTable:

        if sensor['state'] == sensor['newState'] and int(sensor['stateCounter']) == sensor['newStateCounter']:
            continue

        print "updating sensor info "+sensor['id']
        updateSensorState(conn, sensor['id'], sensor['newState'], sensor['newStateCounter'])





def updateSensorState(conn,id,newState,stateCounter):
    """
    """
    cur = conn.cursor()
    cur.execute("""
    update sensor_state
    SET stateName = ?,
        stateCounter = ?
    where sensorId = ? ;
    """, (newState,stateCounter,id))


def restartSensorHits(conn):
    """
    """
    cur = conn.cursor()
    cur.execute("""
    update sensor_hits
    SET counter=0;
    """)

def prepareAlarmMsg(hitsTable):

    msg = ""

    for sensor in hitsTable:

        if sensor['state'] == "ALARM":
            msg += str(sensor['alias']) +" "+ str(sensor['id'])+"\n"

    if msg:
        msg= "myBalcon Alarm!\n"+msg

    print msg



def twitterAlarm(text):

    oauth=expanduser("~/.secrets/twitter")

    try:
        oauth = TwitterOAuth.read_file(oauth)

        api = TwitterAPI(oauth.consumer_key,
                         oauth.consumer_secret,
                         oauth.access_token_key,
                         oauth.access_token_secret)

        #r = api.update_status(status = text) 
        #r = api.request('statuses/update_with_media', {'status':text})
        r = api.request('statuses/update', {'status': text})
        print(r.status_code)


    except KeyboardInterrupt:
        print('Terminated by user')

    except Exception as e:
        print('STOPPED: %s' % e)




 
def main():
    database = "/var/lib/balcon/balcon.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        insertNewSensors(conn)
        hitsTable = select_hits(conn) 
        #print("Min mois of last 24 hours:")
        #select_all_tasks(conn)
        hitsTable=checkHits(hitsTable)
        updateSensorStateTable(conn,hitsTable)

        alarmMsg = prepareAlarmMsg(hitsTable)
        #twitterAlarm(alarmMsg)

        restartSensorHits(conn)
 
 
if __name__ == '__main__':
    main()
    #twitterAlarm("Hi there")