#!/usr/bin/python3

#Install: pip3 install psycopg2 configparser psycopg2-binary
# create user offerseapg with password 'pwd';
#GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO offerseapg;

import psycopg2
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
 #       print('PostgreSQL database version:')
 #       cur.execute('SELECT version()')

        sql = """INSERT INTO jobs(job_no, subject, description, tags) VALUES %s RETURNING job_no;"""
        job=(2, "write script", "write pythone code", "python, coding")
        cur.execute(sql, (job,))

        #sql = """ select * from jobs"""
        #cur.execute(sql)

        # display the PostgreSQL database server version
        db_version = cur.fetchall()
        #conn.commit()
        print(db_version)
        #conn.commit()
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_jobs_list(job_list):
    """ insert multiple jobs into the jobs table  """
    sql = """INSERT INTO jobs(subject, description, tags) VALUES %s RETURNING job_no;"""
    #job_list=(2, "write script", "write pythone code", "python, coding")
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql,(job_list,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
#if __name__ == '__main__':
#    connect()
