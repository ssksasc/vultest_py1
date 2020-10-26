import mysql.connector
import util

'''
create database vultest;
create user 'vultest'@'172.17.0.%' identified by 'vultest.89shiki';
grant all privileges on vultest.* to 'vultest'@'172.17.0.%';
flush privileges;
'''

class MySQL_DB:
    def __init__(self):
        self.cfg = {
            'user': 'vultest',
            'password': 'vultest.89shiki',
            'host': '172.17.0.1',
            'port': '3306',
            'database': 'vultest'
        }
        self.cur = None
        self.con = None
    
    def connect(self):
        self.con = mysql.connector.connect(**(self.cfg))
        self.cur = self.con.cursor()
    
    def close(self):
        self.cur.close()
        self.con.close()

    def query(self, sql, params=()):
        result = None
        try:
            self.cur.execute(sql, params)
            result = self.cur.fetchall()
        except mysql.connector.Error as e:
            ### Error
            util.error('DB query Error', e)
        return result

    def execute(self, sql, params=()):
        result = False
        try:
            self.cur.execute(sql, params)
            self.con.commit()
            result = True
        except mysql.connector.Error as e:
            ### Error
            util.error('DB execute Error', e)
        return result

    def last_insert_id(self):
        return self.cur.lastrowid

db = MySQL_DB()


