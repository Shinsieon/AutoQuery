import MySQLdb as mdb

class dbConnection:
    def __init__(self):
        self.isConnect = False
        self.mdb = mdb
    def setDBinfo(self, dbObj):
        self.host = dbObj['host']
        self.user = dbObj['user']
        self.password = dbObj['password']
        self.dbName = dbObj['dbName']
        self.charset = dbObj['charset']
        
    def openConn(self):
        try :
            self.db = mdb.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                db = self.dbName,
                charset = self.charset
            )
            self.isConnect = True

        except mdb.Error as e:
            self.isConnect = False
