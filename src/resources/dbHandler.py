import mysql.connector
from mysql.connector import errorcode
import logging
import datetime

class DBHandler(object):
    def __init__(self):
        self.logger = self.configure_logging()
        self.connect()

    def connect(self):
        try:
            self.__mySession = mysql.connector.connect(
                host="rendt-database.cksgcmivrysp.us-east-2.rds.amazonaws.com",
                port="3306",
                user='rendtTeam',
                password="rendt-db-admin",
                database='RendtDB')
            self.__mySession.ping(reconnect=True, attempts=1, delay=0)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.error(
                    "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.error("Database does not exist")
            else:
                self.logger.error("ERROR: err")
                exit(1)
        else:
            self.logger.info("connected successfully to db")
            self.__cursor = self.__mySession.cursor(buffered=True)
            self.__cursor.execute("use {}".format(self.__mySession.database))

    def configure_logging(self):
        logger = logging.getLogger('DBHandler.logger')
        logger.setLevel(logging.INFO)

        currentDT = str(datetime.datetime.now()).replace(' ', '_')
        format_ = logging.Formatter('%(asctime)s  %(name)-15s  %(levelname)-8s  %(message)s')

        # create log fle handler
        db_logfile_handler = logging.FileHandler('logs/db_logfile_' + currentDT)
        db_logfile_handler.setLevel(logging.INFO)
        db_logfile_handler.setFormatter(format_)
        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(format_)

        logger.addHandler(console_handler)
        logger.addHandler(db_logfile_handler)

        logger.info('begin log')
        return logger

    def _executeQuery(self, query, dataList=[]):
        try:
            self.__cursor.execute(query, dataList)
            self.__mySession.commit()
        except mysql.connector.Error as err:
            self.logger.warning(
                "Lost connection to database. Trying to reconnect.")
            self.__mySession.reconnect(attempts=3)
            try:
                self.__cursor.execute(query, dataList)
                self.__mySession.commit()
            except mysql.connector.Error as err:
                self.logger.error("DBHandler Error: {}".format(err))
                exit(1)

    def _createNewDB(self, dbName):
        try:
            self.__cursor.execute("create database {} ".format(dbName))
        except mysql.connector.Error as err:
            self.logger.error("Failed creating database: {}".format(err))
            exit(1)

    def _deleteDB(self, dbName):
        try:
            self.__cursor.execute("drop database {} ".format(dbName))
        except mysql.connector.Error as err:
            self.logger.error("Failed deleting database: {}".format(err))
            exit(1)

    def _switchDB(self, dbName):
        try:
            self.__cursor.execute("use {} ".format(dbName))
        except mysql.connector.Error as err:
            self.logger.error("Failed creating database: {}".format(err))
            exit(1)

    def _endSession(self):
        try:
            self.__mySession.close()
            self.__cursor.close()
        except mysql.connector.Error as err:
            self.logger.error(
                "Could not end session successfully: {}".format(err))
            exit(1)

    def getJobs(self, status='a'):
        query = f'SELECT job_id FROM jobs WHERE job_status = "{status}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return [row[0] for row in rows]

    def isFinished(self, job_id):
        query = f'SELECT job_id FROM jobs WHERE job_id = {job_id} AND job_status = "f"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 1
    
    def queryLeasers(self, status='a'):
        # TODO return username and reliability score/uptime/last logged in as well
        query = f'SELECT U.username, L.short_info, L.machine_details, L.price FROM leasers L, users U WHERE L.user_id=U.user_id AND L.status = "{status}"'
        # f'SELECT user_id, machine_details FROM leasers WHERE status = "{status}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows

    def getUserId(self, username):
        query = f'SELECT user_id FROM users WHERE username = "{username}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

    def addJob(self, user_id, job_id, job_type, files_size, token, comments, status='a'):
        # add job to list of jobs
        query = f'INSERT INTO jobs (user_id, job_id, job_type, files_size, job_status, additional_comments) \
                VALUES ({user_id}, {job_id}, "{job_type}", {files_size}, "{status}", "{comments}")'
        self._executeQuery(query)

        # add tokens to renter jobs table
        query = f'INSERT INTO exec_file_tokens (job_id, db_token, file_size) VALUES ({job_id}, "{token}", {files_size})'
        self._executeQuery(query)

    def submitJobOrder(self, order_id, renter_id, job_id, job_mode, leaser_id, status='p'):
        query = f'INSERT INTO job_orders (order_id, renter_id, job_id, job_desc, job_mode, file_size, leaser_id, status) \
                VALUES ({order_id}, {renter_id}, {job_id}, "to be deleted", "{job_mode}", 0, {leaser_id}, "{status}")'
        self._executeQuery(query)

    def updateJobOrderStatus(self, order_id, response):
        query = f'UPDATE job_orders SET status = "{response}" WHERE order_id = {order_id}'
        self._executeQuery(query)

    def getJobRequests(self, leaser_id): # TODO delete job_desc from here
        query = f'SELECT O.order_id, U.username, O.job_id, O.job_desc, O.job_mode, O.status FROM job_orders O, users U WHERE leaser_id = {leaser_id} AND status = "p" AND U.user_id = O.renter_id'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows

    def getOrderJobId(self, order_id):
        query = f'SELECT job_id FROM job_orders WHERE order_id = {order_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows[0][0]

    def getOrderId(self, job_id):
        query = f'SELECT order_id FROM job_orders WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows[0][0]

    def getJobStatus(self, job_id):
        query = f'SELECT job_status FROM jobs WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows[0][0]

    def getJobStatuses(self, renter_id): # TODO delete job_desc from here
        query = f'SELECT O.job_id, O.job_desc, O.job_mode, U.username, O.status FROM job_orders O, users U WHERE O.renter_id = {renter_id} AND O.leaser_id = U.user_id'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows

    def getExecfileToken(self, job_id):
        query = f'SELECT db_token FROM exec_file_tokens WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]
        # TODO else raise or log an error

    def addOutputFileToken(self, job_id, token, file_size):
        query = f'INSERT INTO output_file_tokens (job_id, db_token, file_size) VALUES ({job_id}, "{token}", {file_size})'
        self._executeQuery(query)

    def getOutputToken(self, job_id):
        query = f'SELECT db_token FROM output_file_tokens WHERE job_id = {job_id}'
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
        if token_type == 'x':  # executable
            query = f'SELECT job_id FROM exec_file_tokens WHERE db_token = "{token}"'
        elif token_type == 'o':  # output
            query = f'SELECT job_id FROM output_file_tokens WHERE db_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

    def getAuthToken(self, email):
        user_id = self.getUserInfo(email)[0]
        if user_id:
            query = f'SELECT auth_token FROM active_auth_tokens WHERE user_id = {user_id}'
            self._executeQuery(query)
            rows = self.__cursor.fetchall()
            if len(rows) == 1:
                return rows[0][0]
            
    def addAuthToken(self, user_id, token):
        query = f'INSERT INTO active_auth_tokens (user_id, auth_token) VALUES ({user_id}, "{token}")'
        self._executeQuery(query)        

    def checkAuthToken(self, token):
        query = f'SELECT auth_token FROM active_auth_tokens WHERE auth_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 1

    def getUserIdFromAuthToken(self, token):
        query = f'SELECT user_id FROM active_auth_tokens WHERE auth_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

    def getJobFileSize(self, job_id):
        query = f'SELECT file_size FROM exec_file_tokens WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

    def setJobFileSize(self, job_id, file_size):
        query = f'UPDATE exec_file_tokens SET file_size = {file_size} WHERE job_id = {job_id}'
        self._executeQuery(query)

        query = f'UPDATE jobs SET files_size = {file_size} WHERE job_id = {job_id}'
        self._executeQuery(query)

    def getOutputFileSize(self, job_id):
        query = f'SELECT file_size FROM output_file_tokens WHERE job_id = {job_id}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

    # Blacklist holds expired aythentication tokens alongside the user id
    def addAuthTokenToBList(self, user_id, token):
        query = f'INSERT INTO archived_auth_tokens (user_id, auth_token) VALUES ({user_id}, "{token}")'
        self._executeQuery(query)

    def getAuthTokenFromBList(self, token):
        query = f'SELECT auth_token FROM archived_auth_tokens WHERE auth_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return rows

    def checkAuthTokenAvailability(self, token):
        query = f'SELECT auth_token FROM active_auth_tokens WHERE auth_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 0

    def checkOrderIdAvailability(self, oid):
        query = f'SELECT order_id FROM job_orders WHERE order_id = {oid}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 0
    
    def checkAuthTokenBList(self, token):
        query = f'SELECT auth_token FROM archived_auth_tokens WHERE auth_token = "{token}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 0

    def registerUser(self, user_id, email, pswd, username, user_type='U', chars=' '):
        query = f'INSERT INTO users (user_id, email_address, username, user_type, machine_chpasswordsars) VALUES ({user_id}, "{email}", "{username}", "{user_type}", "{chars}")'
        self._executeQuery(query)

        query = f'INSERT INTO passwords (email_address, password_hash) VALUES ("{email}", "{pswd}")'
        self._executeQuery(query)

    def checkEmailAvailability(self, email):
        query = f'SELECT user_id FROM users where email_address="{email}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 0

    def checkUserIdAvailability(self, uid):
        query = f'SELECT user_id FROM users where user_id={uid}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 0

    def checkJobIdAvailability(self, jid):
        query = f'SELECT job_id FROM jobs where job_id={jid}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        return len(rows) == 0

    def checkDBTokenAvailability(self, token):
        query = f'SELECT job_id FROM exec_file_tokens where db_token="{token}"'
        self._executeQuery(query)
        rows_exec = self.__cursor.fetchall()

        query = f'SELECT job_id FROM output_file_tokens where db_token="{token}"'
        self._executeQuery(query)
        rows_out = self.__cursor.fetchall()

        return len(rows_exec) + len(rows_out) == 0

    def getStoredPasswordHash(self, email):
        query = f'SELECT password_hash FROM passwords WHERE email_address="{email}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0][0]

    def getUserInfo(self, email):
        query = f'SELECT user_id, username, user_type FROM users WHERE email_address="{email}"'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1:
            return rows[0]

    def setLeaserStatus(self, uid, status):
        if self.canLease(uid):
            query = f'UPDATE leasers SET status = "{status}" WHERE user_id = {uid}'
            self._executeQuery(query)
            return True
        return False

    def setExecStartTime(self, order_id, formatted_date):
        query = f'UPDATE job_orders SET exec_start_time = "{formatted_date}" WHERE order_id = {order_id}'
        self._executeQuery(query)

    def setExecFinishTime(self, order_id, formatted_date):
        query = f'UPDATE job_orders SET exec_finish_time = "{formatted_date}" WHERE order_id = {order_id}'
        self._executeQuery(query)

    def markAvailable(self, uid, oneliner, full_machine_info, hourly_rate):
        # if self.canLease(uid): # TODO check if user is a leaser or not
        query = f'SELECT user_id FROM leasers WHERE user_id = {uid}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1: # user is in the leasers list
            query = f'UPDATE leasers SET status = "a" WHERE user_id = {uid}'
            self._executeQuery(query)
            query = f'UPDATE leasers SET short_info = "{oneliner}" WHERE user_id = {uid}'
            self._executeQuery(query)
            query = f'UPDATE leasers SET machine_details = "{full_machine_info}" WHERE user_id = {uid}'
            self._executeQuery(query)
            query = f'UPDATE leasers SET price = {hourly_rate} WHERE user_id = {uid}'
            self._executeQuery(query)
            return True
        else:
            query = f'INSERT INTO leasers (user_id, status, short_info, machine_details, price) VALUES ({uid}, "a", "{oneliner}", "{full_machine_info}", {hourly_rate})'
            self._executeQuery(query)
            return True

    def markUnavailable(self, uid):
        # if self.canLease(uid): # TODO check if user is a leaser or not
        query = f'SELECT user_id FROM leasers WHERE user_id = {uid}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1: # user is in the leasers list
            query = f'UPDATE leasers SET status = "u" WHERE user_id = {uid}'
            self._executeQuery(query)
            return True
        else:
            query = f'INSERT INTO leasers (user_id, status, machine_details) VALUES ({uid}, "u", "test")'
            self._executeQuery(query)
            return True

    def canLease(self, uid):
        '''
        check if user is a leaser and isn't running any jobs(?)
        '''
        query = f'SELECT user_id FROM leasers WHERE user_id = {uid}'
        self._executeQuery(query)
        rows = self.__cursor.fetchall()
        if len(rows) == 1: # user is a leaser
            # TODO maybe do more checks
            return True
