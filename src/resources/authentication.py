import os
import hashlib
import binascii
import string
import random
from dbHandler import DBHandler

class Authentication(object):
    def __init__(self):
        self.HASH_ITERATIONS = 100000
        self.HASH_ALGO = 'sha512'

        self.db_handler = DBHandler()
    
    def register_user(self, email, password):
        if self.db_handler.checkEmailAvailability(email):
            user_id = self.generate_user_id()
            pswd = self.__hash_password(password)
            self.db_handler.registerUser(user_id, email, pswd)
            authToken = self.generate_auth_token()
            self.db_handler.addAuthToken(user_id, authToken)
            return (user_id, authToken)
        else:
            return 1

    def sign_in_user(self, email, password, uid):
        authToken = self.db_handler.getAuthToken(email)
        if authToken:
            print('authToken exists:', authToken)
            return authToken
        else:
            print('authToken doesnot exist')
            stored_password = self.db_handler.getStoredPasswordHash(email)
            if self.__verify_password(stored_password, password):
                authToken = self.generate_auth_token()
                self.db_handler.addAuthToken(uid, authToken)
                return authToken
            else:
                return 1

    def __hash_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac(self.HASH_ALGO, password.encode('utf-8'), salt, self.HASH_ITERATIONS)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def __verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac(self.HASH_ALGO, 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    self.HASH_ITERATIONS)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def generate_user_id(self):
        usrid = int(random.random()*900000)+100000
        while not self.db_handler.checkUserIdAvailability(usrid):
            usrid = int(random.random()*900000)+100000
        return usrid
    
    def generate_auth_token(self):
        chars = string.ascii_letters + string.digits	
        token = ''.join(random.choice(chars) for i in range(13))
        while not self.db_handler.checkAuthTokenAvailability(token) or not self.db_handler.checkAuthTokenBList(token):
            token = ''.join(random.choice(chars) for i in range(13))
        return token