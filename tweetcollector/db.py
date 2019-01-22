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
        self.create_table()
        self.all = self.get_all()
    
    def connect(self):
        self.connection = psycopg2.connect(
            "dbname='%s' user='%s' host='%s' password='%s'"
            %(dbname,user,host,password))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_command = ("CREATE TABLE tweet(id serial PRIMARY KEY, id_twitter varchar(50),\
        name varchar(500), text varchar(500), image varchar(300), followers integer, location varchar(200),\
        classification varchar(216));")
        try:
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
        except:
            pass

    def get_all(self):
        print('Waiting for query execution')
        sql = "SELECT id_twitter,text FROM public.tweet ORDER BY id ASC"
        self.cursor.execute(sql)
        all = [r for r in self.cursor.fetchall()]
        return all

    def save(self, id_twitter,name,text,image,followers,location):
        if self.st.sentiment_avg(text):
            diff = self.close_matches(text)
            if diff:
                pass
            else:
                self.all.append((id_twitter,text))
                self.insert(id_twitter,name,text,image,followers,location)
    
    def delete(self, id):
        sql = "DELETE FROM public.tweet WHERE id = %s" %id
        self.cursor.execute(sql)

    def close_matches(self, text):
        matches = []
        rage_text = int(len(text)/3)
        for i in self.all:
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

    def save_data(self, result):
        try:
            text = result.retweeted_status.full_text
        except:
            text = result.full_text
        id_twitter = result.id
        name = result.user.screen_name
        img = result.user.profile_image_url
        followers = result.user.followers_count
        location = result.user.location
        self.save(id_twitter,name,text,img,followers,location)

    def str_(self,string):
        string = str(string)
        string = string.encode('utf-8').decode('utf-8')
        string = string.replace("'","´")
        string = string.replace('"',"\"")
        return string
