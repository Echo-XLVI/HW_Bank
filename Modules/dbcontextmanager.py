from databaseconnection import DBConnection

class ContextManager:
    def __init__(self,config:dict) -> None:
        self.config=config
        self.connection_obj=None

    def __enter__(self):
        dbconnect=DBConnection(self.config)
        dbconnect.create_connection()
        dbconnect.create_cursor()
        self.connection_obj=dbconnect
        return self.connection_obj

    def __exit__(self,exc_type,exc_value,exc_traceback):
        if exc_type or exc_value or exc_traceback:
            self.connection_obj.connection.rollback()
            print(exc_type,exc_value,exc_traceback)
        else:
          self.connection_obj.connection.commit()
          self.connection_obj.close_connection()
          self.connection_obj.close_cursor()