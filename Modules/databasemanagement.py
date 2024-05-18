from dbcontextmanager import ContextManager

class DataBaseManager:

    config={
         'dbname':'bank',
         'host':'localhost',
         'port':5648,
         'user':'postgres',
         'password':'1380ACreZA46'
    }

    @classmethod
    def insert_user(cls, user_id:str, username:str, password:int) -> None:
        query=f"Insert Into users (user_id,username,password) Values ('{user_id}', '{username}', '{password}')"
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
    def insert_account(cls, user_id:str, account_id:str, balance:int):
        query=f"Insert Into account values('{account_id}','{user_id}',{balance})"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)

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
    def check_balance(cls, account_id:str) -> tuple:
        query=f"Select balance from account Where account_id='{account_id}'"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            res=db.cursor.fetchone()
        if res:
            return res
        else:
            return None

    @classmethod
    def deposit(cls, account_id:str, amount:int) -> None:
        query=f"Update account Set balance = balance + {amount} Where account_id = '{account_id}'"
        query2=f"Insert Into transaction(account_id,amount,transaction_type,timestamp) Values('{account_id}',{amount},'deposit',CURRENT_TIMESTAMP)"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            db.cursor.execute(query2)

    @classmethod
    def withdraw(cls, account_id:str, amount:int) -> None:
        query=f"Update account Set balance = balance - {amount} Where account_id = '{account_id}'"
        query2=f"Insert Into transaction(account_id,amount,transaction_type,timestamp) Values('{account_id}',{amount},'withdrawal',CURRENT_TIMESTAMP)"
        with ContextManager(cls.config) as db:
            db.cursor.execute(query)
            db.cursor.execute(query2)

##################################################
# DataBaseManager.check_username('reza')
# DataBaseManager.login_query('reza','1380ACreza')