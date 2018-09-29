import psycopg2
from pprint import pprint

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='twitter-database' user='postgres' host='localhost' password='admin' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Failure in connection")
        try:
            create_table_command = ("CREATE TABLE tweet(id serial PRIMARY KEY, id_twitter varchar(50), name varchar(500), text varchar(500), image varchar(300), followers integer, location varchar(100), classification varchar(216));")
            self.cursor.execute(create_table_command)
            print('Table created')
        except:
            pass

    def insert_new(self,id_twitter, nome, texto, imagem, seguidores, localizacao, classification):
        insert_command = ("INSERT INTO tweet(id_twitter, name, text, image, followers, location, classification) VALUES('%s','%s','%s','%s','%d','%s','%s')" 
        %(id_twitter, nome, texto, imagem, seguidores, localizacao,classification))
        self.cursor.execute(insert_command)
