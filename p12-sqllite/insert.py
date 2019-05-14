
import sqlite3
from sqlite3 import Error



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None



def add_reading(conn, reading):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' insert or ignore INTO reading (sensorId,nameId,value,datetime)
              VALUES(?,?,?,?); '''
    cur = conn.cursor()
    cur.execute(sql, reading)
    return cur.lastrowid




def main():
    database = "./balcon.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        # add temp
        r = ('ESP111', 'Temp', '22.1', '2015-01-02 12:12')
        r_id = add_reading(conn, r)
        print r_id


if __name__ == '__main__':
    main()