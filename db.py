import psycopg2
from pprint import pprint

class Database:
    def __init__(self, nome, texto, imagem, seguidores, localizacao):
        self.nome = str(nome)
        self.texto = str(texto)
        self.imagem = str(imagem)
        self.seguidores = str(seguidores)
        self.localizacao = str(localizacao)

        try:
            self.connection = psycopg2.connect(
                "dbname='twitter-database' user='postgres' host='localhost' password='admin' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Failure in connection")

    def create_table(self):
        create_table_command = ("CREATE TABLE tweet(id serial PRIMARY KEY, name varchar(100), text varchar(500), image varchar(100), followers varchar(100), location varchar(100), classification varchar(3));")
        try:
            self.cursor.execute(create_table_command)
            print('Table created')
        except:
            pass

    def insert_new(self):
        insert_command = ("INSERT INTO tweet(name, text, image, followers, location) VALUES('%s','%s','%s','%s','%s')" 
        %(self.nome, self.texto, self.imagem, self.seguidores, self.localizacao))
        self.cursor.execute(insert_command)
