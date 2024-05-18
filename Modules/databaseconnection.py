import psycopg2

class DBConnection:
    def __init__(self,config:dict) -> None:
        self.config=config
        self.connection=None
        self.cursor=None

    def create_connection(self) -> None:
        if not self.connection:
            self.connection=psycopg2.connect(**self.config)
            
    def create_cursor(self):
        if not self.cursor:
            self.cursor=self.connection.cursor()

    def close_connection(self):
        self.connection.close()
    
    def close_cursor(self):
        self.cursor.close()
    
    def close(self):
        self.connection.close()
        self.cursor.close()