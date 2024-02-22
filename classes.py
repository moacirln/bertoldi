import psycopg2 as pg2

class BD:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        # Tenta estabelecer uma conexão; armazena a conexão e o cursor como atributos
        try:
            self.conn = pg2.connect(database='poscalc', user='postgres', password='Moacir66,', host='bertoldi.c1wwgyau8nj4.us-east-2.rds.amazonaws.com', port='5432')
            self.cur = self.conn.cursor()
        except pg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None
            self.cur = None

    def disconnect(self):
        # Fecha o cursor e a conexão se eles existirem
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
