from databaseconnection import DBConnection
from bankaccount_module import BankAccount
from user_module import User

class ModelManager:
    def __init__(self, db_manager_obj, table_name:str, model_class:object):
        self.db_manager = db_manager_obj
        self.table_name = table_name
        self.model_class = model_class

    def get():
        pass

    def filter():
        pass

    def update():
        pass

    def delete():
        pass


class AccountManager(ModelManager):
    def __init__(self, db_manager_obj:DBConnection) -> None:
        super().__init__(db_manager_obj, "accounts", BankAccount)

    def create_account(self, user_obj:object, balance:int) -> None:
        if not DataBaseManager.check_userid_account(user_obj.user_id):
            acc_obj=BankAccount(user_obj.user_id, balance)
            user_obj.acc_obj=acc_obj
            DataBaseManager.insert_account(user_obj.user_id, balance)
        else:
            print("You've already created an acoount!!!")

    def deposit(self, user_obj:object, amount:int) -> None:
        DataBaseManager.deposit(user_obj.acc_obj.acc_id, amount)

    def withdraw(self, user_obj:object, amount:int) -> None:
        balance=int(DataBaseManager.check_balance(user_obj.acc_obj.acc_id)[0])
        if balance>amount:
            DataBaseManager.withdraw(user_obj.acc_obj.acc_id, amount)
        else:
            print('Insufficient Funds')

class UserManager(ModelManager):
    def __init__(self, db_manager_obj:DBConnection) -> None:
        super().__init__(db_manager_obj,'users',User)

    def register(self, username:str, password:str) -> None:
        if not dbm.check_username(username):
            dbm.insert_user(username,password)
            User(user_id,username,password)
        else:
            print('This username already exists try again!!!')

    def login(self, username:str, password:str) -> object:
        res=dbm.login_query(username, password)

        if res:
            if res[0] and res[1]:
                                                                    ## if logged in user already has created account
                bank_obj=BankAccount(res[1][0], res[1][1], int(res[1][2])) 
                return User(res[0][0], res[0][1], res[0][2], bank_obj)
            else:
                return User(res[0][0], res[0][1], res[0][2])
        else:
            return None      

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

class DataBaseManager:

    config={
         'dbname':'bank',
         'host':'localhost',
         'port':5648,
         'user':'postgres',
         'password':'1380ACreZA46'
    }

    @classmethod
    def insert_user(cls, username:str, password:int) -> None:
        query=f"Insert Into users (username,password) Values ('{username}', '{password}')"
        with ContextManager(cls.config) as db:
             db.cursor.execute(query)
    
    @classmethod
    def check_id(cls, user_id:str) -> bool:
        query=f" Select user_id From users Where user_id='{user_id}';"
        with ContextManager(cls.config)  as db:
            db.cursor.execute(query)
            result=db.cursor.fetchone()
        if result:
            return True
        else:
          return False 
    
    @classmethod
    def check_username(cls, username:str) -> bool:
        query=f" Select username From users where username='{username}'";
        with ContextManager(cls.config)  as db:
            db.cursor.execute(query)
            result=db.cursor.fetchone()
        if result:    
            return True
        else:
            return False 
    
    @classmethod
    def login_query(cls, username:str, password:str) -> tuple:
            query = f"Select * From users Where username='{username}' And password='{password}'"
            query2 = """Select * From account Where user_id = %s"""
            with ContextManager(cls.config)  as db:
                                                        ## To fetch user details
                db.cursor.execute(query)
                result = db.cursor.fetchone()
                                                        ## To fetch account details
                param=(result[0],)
                db.cursor.execute(query2,param)
                result2 = db.cursor.fetchone()
            return result,result2 
    
    @classmethod
    def insert_account(cls, user_id:str, balance:int):
        query="Insert Into account (user_id, balance) values(%s, %s)"
        params=(user_id, balance)
        with ContextManager(cls.config) as db:
            db.cursor.execute(query, params)

    @classmethod
    def check_accountid(cls, account_id:str) -> bool:
        query=f"Select * from account Where account_id='{account_id}'"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            result=db.cursor.fetchone()
        if result:    
            return True
        else:
            return False 

    @classmethod
    def check_userid_account(cls, user_id:str) -> bool:    
        query=f"Select * From account Where user_id='{user_id}'"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            result=db.cursor.fetchone()
        if result:    
            return True
        else:
            return False 
    
    @classmethod
    def check_balance_query(cls, account_id:str) -> tuple:
        query=f"Select balance from account Where account_id='{account_id}'"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            res=db.cursor.fetchone()
        if res:
            return res
        else:
            return None

    @classmethod
    def deposit_query(cls, account_id:str, amount:int) -> None:
        query=f"Update account Set balance = balance + {amount} Where account_id = '{account_id}'"
        query2=f"Insert Into transaction(account_id,amount,transaction_type,timestamp) Values('{account_id}',{amount},'deposit',CURRENT_TIMESTAMP)"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            db.cursor.execute(query2)

    @classmethod
    def withdraw_query(cls, account_id:str, amount:int) -> None:
        query=f"Update account Set balance = balance - {amount} Where account_id = '{account_id}'"
        query2=f"Insert Into transaction(account_id,amount,transaction_type,timestamp) Values('{account_id}',{amount},'withdrawal',CURRENT_TIMESTAMP)"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            db.cursor.execute(query2)

    # TODO:write a transfer method
    def transfer_query(cls, amount:int, to_account_id:int):
        query_des_acc = "Update accounts Set balance=balance+%s where account_id=%s"
        query_org_acc = "Update accounts Set balance=balance-%s where account_id=%s"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query_des_acc)
            db.cursor.execute(query_org_acc)
    
    def 