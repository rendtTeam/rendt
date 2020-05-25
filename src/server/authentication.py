import random
from dbHandler import DBHandler
from Crypto import Random
from Crypto.PublicKey import RSA
import hashlib
import jwt
"""
Incase of getting an error of: NotImplementedError: Algorithm 'RS256' could not be found. 
Check either you have cryptography installed, if not:
try: pip install cryptography
"""

class Authentication(object):

    def __init__(self):
        self.__dbSession = DBHandler()

    def createAuthToken(self):
        #generate random token from os.random
        self.__authToken = random.randrange(1000000000, 10000000000000000000)
        self.__rowsAuthToken = self.__checkAuthToken(self.__authToken)
        self.__rowsAuthTokenBList = self.__checkAuthTokenBList(self.__authToken)
        while len(self.__rowsAuthToken) != 0 or len(self.__rowsAuthTokenBList) != 0:
            self.__authToken = random.randrange(1000000000, 10000000000000000000)
            self.__rowsAuthToken = self.__checkAuthToken(self.__authToken)
            self.__rowsAuthTokenBList = self.__checkAuthTokenBList(self.__authToken)

        return self.__authToken

    def __checkAuthToken(self, token):
        # self.__dbSession = DBHandler()
        self.__rows = self.__dbSession.getAuthToken(token)
        return self.__rows
    
    def __checkAuthTokenBList(self, token):
        # self.__dbSession = DBHandler()
        self.__rows = self.__dbSession.getAuthTokenFromBList(token)
        return self.__rows
    
    # Returns keys in PEM format
    def generateSecurityKey(self):
        self.__randomGenerator = Random.new().read
        self.__RSAKey = RSA.generate(1024, self.__randomGenerator)
        self.__privateKey = self.__RSAKey.export_key()
        self.__publicKey = self.__RSAKey.publickey().exportKey()
        return self.__privateKey, self.__publicKey

    def hashPublicKey(self, publicKey):
        self.__hashObject = hashlib.sha256(publicKey)
        self.__hexDigest = self.__hashObject.hexdigest()
        return self.__hexDigest
    
    def convertToRSAkey(self, publicKey):
        self.__serverPublicKey = RSA.importKey(publicKey)
        return self.__serverPublicKey

    def encodeUsingJWTDefault(self, payload, secretKey):
        self.__encoded = jwt.encode(payload, secretKey, algorithm = 'HS256')
        return self.__encoded
    
    def decodeUsingJWTDefault(self, encoded, secretKey):
        self.__decoded = jwt.decode(encoded, secretKey, algorithm = 'HS256')
        return self.__decoded
    
    def encodeUsingRSAKeys(self, payload, secretKey):
        self.__encoded = jwt.encode(payload, secretKey, algorithm = 'RS256')
        return self.__encoded
    
    def decodeUsingRSAKeys(self, encoded, secretKey):
        self.__decoded = jwt.decode(encoded, secretKey, algorithm = 'RS256')
        return self.__decoded
    

    




x = Authentication()
# y = x.createAuthToken()
# print(y)

"""Checking RSA keys"""
privateKey, publicKey = x.generateSecurityKey()
# print(type(publicKey))
# print (privateKey)
# print (publicKey)
# print (x.convertToRSAkey(privateKey))
# print (x.convertToRSAkey(publicKey))
# print (x.hashPublicKey(publicKey))

"""Checking jwt default enc/dec"""
# payload = {"auth": "my message to be encoded and decoded"}
# enc = x.encodeUsingJWTDefault(payload, "alma")
# print(enc)
# dec = x.decodeUsingJWTDefault(enc, "alma")
# print(dec)

"""Checking jwt RSA enc/dec"""
payload2 = {"auth": "my message to be encoded and decoded"}
rsaenc = x.encodeUsingRSAKeys(payload2, privateKey)
# # print(rsaenc)
# pKey = {"pkey":publicKey.decode("utf-8")}
# enPubKey = x.encodeUsingJWTDefault(pKey, "a")
# dePubKey = x.decodeUsingJWTDefault(enPubKey, "a")
# print (dePubKey["pkey"])
rsadec = x.decodeUsingRSAKeys(rsaenc, publicKey)
print(rsadec)

# print("priv: {} , pub: {}".format(privateKey,publicKey))