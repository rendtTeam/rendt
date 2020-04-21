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
    
    def queryJobs(self, status='a'):
        query = f'SELECT job_id FROM jobs WHERE job_status = "{status}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return [row[0] for row in rows]

    def addJob(self, user_id, job_id, job_type, files_size, token, status='a', comments=''):
        # add job to list of jobs
        query = f'INSERT INTO jobs (user_id, job_id, job_type, files_size, job_status, additional_comments) \
                VALUES ({user_id}, {job_id}, "{job_type}", {files_size}, "{status}", "{comments}")'
        self._executeQuery(query)

        # add tokens to renter jobs table
        query = f'INSERT INTO storage_tokens (job_id, db_token) VALUES ({job_id}, "{token}")'
        self._executeQuery(query)

    def getExecfileToken(self, job_id):
        query = f'SELECT db_token FROM storage_tokens WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]
        # TODO else raise or log an error

    def addOutputFileToken(self, job_id, token):
        query = f'INSERT INTO outputFile_tokens (job_id, db_token) VALUES ({job_id}, "{token}")'
        self._executeQuery(query)

    def getOutputToken(self, job_id):
        query = f'SELECT db_token FROM outputFile_tokens WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]
        # TODO else raise or log an error

    def changeJobStatus(self, job_id, status):
        query = f'UPDATE jobs SET job_status = "{status}" WHERE job_id = {job_id}'
        self._executeQuery(query)

    def getUserJobs(self, user_id, status='all'):
        if status == 'all':
            query = f'SELECT job_id FROM jobs WHERE user_id = {user_id}'
        else:
            query = f'SELECT job_id FROM jobs WHERE user_id = {user_id} AND job_status = "{status}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return [row[0] for row in rows]

    # rendundant after storage is set up and we no longer address file addresses using job_ids
    def getJobIdFromToken(self, token, token_type):
        if token_type == 'x': # executable
            query = f'SELECT job_id FROM storage_tokens WHERE db_token = "{token}"'
        elif token_type == 'o': # output
            query = f'SELECT job_id FROM outputFile_tokens WHERE db_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

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
    
    def addAuthToken(self, user_id, token):
        query = f'INSERT INTO authentication_token (user_id, auth_token) VALUES ({user_id}, "{token}")'
        self._executeQuery(query)

    def getAuthToken(self, token):
        query = f'SELECT auth_token FROM authentication_token WHERE auth_token = {token}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows
    
    # Blacklist holds expired aythentication tokens alongside the user id 
    def addAuthTokenToBList(self, user_id, token):
        query = f'INSERT INTO authentication_token_blacklist (user_id, auth_token_blist) VALUES ({user_id}, "{token}")'
        self._executeQuery(query)

    def getAuthTokenFromBList(self, token):
        query = f'SELECT auth_token_blist FROM authentication_token_blacklist WHERE auth_token_blist = {token}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows

    """
    def getSessionHandler(self):
        return self.__mySession
    """