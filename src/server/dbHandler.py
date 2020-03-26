import mysql.connector
from mysql.connector import errorcode

class DBHandler(object):
    def __init__(self):
        try:
            self.__mySession = mysql.connector.connect(
                host = "rendt-database.cksgcmivrysp.us-east-2.rds.amazonaws.com",
                port = "3306",
                user = 'rendtTeam',
                password = "rendt-db-admin",
                database = 'RendtDB')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                exit(1)
        else:
            print("connected successfully to db")
            self.__cursor = self.__mySession.cursor(buffered=True)
            self.__cursor.execute("use {}".format(self.__mySession.database))
    
    def queryJobs(self, status='available'):
        query = f'SELECT job_id FROM jobs WHERE job_status = "{status}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return [row[0] for row in rows]

    def addJob(self, job_id, job_type, loc, token, status='available', comments=''):
        query = f'INSERT INTO jobs (job_id, job_type, location_of_exec_files, db_token, job_status, additional_comments) \
                VALUES ({job_id}, "{job_type}", "{loc}", {token}, "{status}", "{comments}")'
        self._executeQuery(query)

    def changeJobStatus(self, job_id, status):
        query = f'UPDATE jobs SET job_status = "{status}" WHERE job_id = {job_id}'
        self._executeQuery(query)

    def _executeQuery(self, query, dataList=[]):
        try:
            self.__cursor.execute(query, dataList)
            self.__mySession.commit()
        except mysql.connector.Error as err:
            print("Failed executing query: {}".format(err))
            exit(1)
    
    def _createNewDB(self, dbName):
        try:
            self.__cursor.execute("create database {} ".format(dbName))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
            
    def _deleteDB(self, dbName):
        try:
            self.__cursor.execute("drop database {} ".format(dbName))
        except mysql.connector.Error as err:
            print("Failed deleting database: {}".format(err))
            exit(1)

    def _switchDB(self, dbName):
        try:
            self.__cursor.execute("use {} ".format(dbName))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
    
    def _endSession(self):
        try:
            self.__mySession.close()
            self.__cursor.close()
        except mysql.connector.Error as err:
            print("Could not end session successfully: {}".format(err))
            exit(1)
    """
    def getSessionHandler(self):
        return self.__mySession
    """