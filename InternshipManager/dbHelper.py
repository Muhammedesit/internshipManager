import mysql.connector

class DbHelper():
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "Say.My_n4m3"
        self.database = 'internship'
        
    def getConnection(self):

        connection = mysql.connector.connect(host = "localhost",
                                    user='root', 
                                    password = "Say.My_n4m3",
                                    database='internship', )
        return connection

