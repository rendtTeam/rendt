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
            self.__cursor = self.__mySession.cursor()
            self.__cursor.execute("use {}".format(self.__mySession.database))
    
    def executeQuery(self, query, dataList):
        try:
            self.__cursor.execute(query, dataList)
            self.__mySession.commit()
        except mysql.connector.Error as err:
            print("Failed executing query: {}".format(err))
            exit(1)
    
    def createNewDB(self, dbName):
        try:
            self.__cursor.execute("create database {} ".format(dbName))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
            
    def deleteDB(self, dbName):
        try:
            self.__cursor.execute("drop database {} ".format(dbName))
        except mysql.connector.Error as err:
            print("Failed deleting database: {}".format(err))
            exit(1)

    def switchDB(self, dbName):
        try:
            self.__cursor.execute("use {} ".format(dbName))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
    
    def endSession(self):
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