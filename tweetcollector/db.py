import psycopg2, difflib, time
from unicodedata import normalize
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
        create_table_command = ("CREATE TABLE IF NOT EXISTS tweets(id serial PRIMARY KEY, id_twitter varchar(50),\
        name varchar(500), text varchar(500), image varchar(300), followers integer, location varchar(200),\
        classification varchar(216), query varchar(200));")
        self.cursor.execute(create_table_command)

    def insert(self,id_twitter,name,text,image,followers,location, query):
        insert_command = ("INSERT INTO tweets(id_twitter, name, text, image, followers, location, query)\
         VALUES('%s','%s','%s','%s','%d','%s','%s')" 
        %(id_twitter,self.str_(name),self.str_(text),image,followers,self.str_(location), query))
        self.cursor.execute(insert_command)

    def get_all(self):
        sql = "SELECT id_twitter,text FROM public.tweets ORDER BY id ASC"
        self.cursor.execute(sql)
        all = [r for r in self.cursor.fetchall()]
        return all

    def main(self, id_twitter,name,text,image,followers,location, query):
        if self.st.sentiment_avg(text):
            diff = self.close_matches(text)
            if diff:
                pass
            else:
                self.all.append((id_twitter,text))
                self.insert(id_twitter,name,text,image,followers,location, query)
    
    def delete(self, id):
        sql = "DELETE FROM public.tweets WHERE id = %s" %id
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

    def save(self, result, query):
        try:
            text = result.retweeted_status.full_text
        except:
            text = result.full_text
        id_twitter = result.id
        name = result.user.screen_name
        img = result.user.profile_image_url
        followers = result.user.followers_count
        location = result.user.location
        self.main(id_twitter,name,text,img,followers,location, query)

    def str_(self,string):
        string = str(string)
        string = string.encode('utf-8').decode('utf-8')
        string = string.replace("'","´")
        string = string.replace('"',"\"")
        return string
