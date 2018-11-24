import psycopg2, difflib
from auth import dbname,host,password,port,user

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='%s' user='%s' host='%s' password='%s'"
                %(dbname,user,host,password))
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print("Failure in connection")
            
    def create_table(self):
        try:
            create_table_command = ("CREATE TABLE tweet(id serial PRIMARY KEY, id_twitter varchar(50),\
             name varchar(500), text varchar(500), image varchar(300), followers integer, location varchar(200),\
             classification varchar(216));")
            self.cursor.execute(create_table_command)
            print('Table created')
        except:
            pass
    def save(self,id_twitter,name,text,image,followers,location):
        insert_command = ("INSERT INTO tweet(id_twitter, name, text, image, followers, location)\
         VALUES('%s','%s','%s','%s','%d','%s')" 
        %(id_twitter,self.str_(name),self.str_(text),image,followers,self.str_(location)))
        try:
            self.cursor.execute(insert_command)
        except:
            pass

    def matches(self, text):
        sql = "SELECT text FROM public.tweet ORDER BY id ASC"
        self.cursor.execute(sql)
        all = [r[0] for r in self.cursor.fetchall()]
        diff = difflib.get_close_matches(text, all)
        if diff:
            return False
        else:
            return True

    def str_(self,string):
        string = str(string)
        string = string.encode('utf-8').decode('utf-8')
        string = string.replace("'","\'")
        string = string.replace('"',"\"")
        return string
