import psycopg2, difflib, time
from unicodedata import normalize
from tweetcollector.report import Report
from auth import dbname,host,password,port,user
from tweetcollector.senticnet_instance import Sentiment


class Database:
    def __init__(self):
        self.st = Sentiment()
        try:
            self.connect()
        except:
            print("Failure in connection")
    
    def connect(self):
        self.connection = psycopg2.connect(
            "dbname='%s' user='%s' host='%s' password='%s'"
            %(dbname,user,host,password))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            create_table_command = ("CREATE TABLE tweet(id serial PRIMARY KEY, id_twitter varchar(50),\
             name varchar(500), text varchar(500), image varchar(300), followers integer, location varchar(200),\
             classification varchar(216));")
            self.cursor.execute(create_table_command)
            print('Table created')
        except:
            self.connect()

    def insert(self,id_twitter,name,text,image,followers,location):
        insert_command = ("INSERT INTO tweet(id_twitter, name, text, image, followers, location)\
         VALUES('%s','%s','%s','%s','%d','%s')" 
        %(id_twitter,self.str_(name),self.str_(text),image,followers,self.str_(location)))
        try:
            self.cursor.execute(insert_command)
        except UnicodeEncodeError:
            self.connect()
            insert_command = ("INSERT INTO tweet(id_twitter, name, text, image, followers, location)\
            VALUES('%s','%s','%s','%s','%d','%s')" 
            %(id_twitter,self.normalize(name),self.normalize(text),image,followers,self.normalize(location)))
            self.cursor.execute(insert_command)

    def get_all(self):
        print('Waiting for query execution')
        sql = "SELECT id_twitter,text FROM public.tweet ORDER BY id ASC"
        self.cursor.execute(sql)
        all = [r for r in self.cursor.fetchall()]
        return all

    def save(self, id_twitter,name,text,image,followers,location, all):
        if self.st.sentiment_avg(text):
            diff = self.close_matches(text, all)
            if diff:
                pass
            else:
                all.append((id_twitter,text))
                self.insert(id_twitter,name,text,image,followers,location)
                time.sleep(3)

    def delete(self, id):
        sql = "DELETE FROM public.tweet WHERE id = %s" %id
        self.cursor.execute(sql)

    def close_matches(self, text,all):
        matches = []
        rage_text = int(len(text)/3)
        for i in all:
            count = 0
            for y in range(rage_text):
                try:
                    if i[1][y]==text[y]:
                        count+=1
                except:
                    break
                if y == 0 and count==0:
                    break
            if count == rage_text:
                matches.append(i)
        return matches

    def str_(self,string):
        string = str(string)
        string = string.encode('utf-8').decode('utf-8')
        string = string.replace("'","\'")
        string = string.replace('"',"\"")
        return string

    def normalize(self,string):
        string = self.str_(string)
        return normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')
