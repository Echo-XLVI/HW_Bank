from bankaccount_module import BankAccount
from user_module import User

#TODO: make this class a dynamic query base
class ModelManager:
    def __init__(self, db_manager_obj, table_name:str, model_class:object):
        self.db_manager_obj = db_manager_obj
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
    def __init__(self, db_manager_obj) -> None:
        super().__init__(db_manager_obj, "accounts", BankAccount)

    def create_account(self, user_obj:object, account_type:str, balance:int) -> None:
        if not self.db_manager_obj.check_userid_account(user_obj.user_id):
            acc_obj=BankAccount(user_obj.user_id, account_type, balance)
            user_obj.acc_obj=acc_obj
            self.db_manager_obj.insert_account(user_obj.user_id, account_type, balance)
        else:
            print("You've already created an acoount!!!")

    def deposit(self, user_obj:object, amount:int) -> None:
        self.db_manager_obj.deposit(user_obj.acc_obj.acc_id, amount)

    def withdraw(self, user_obj:object, amount:int) -> None:
        balance=int(self.db_manager_obj.check_balance(user_obj.acc_obj.acc_id)[0])
        if balance>amount:
            self.db_manager_obj.withdraw(user_obj.acc_obj.acc_id, amount)
        else:
            print('Insufficient Funds')
    
    def transfer(self, user_obj:object,  to_account_id:int, amount:int) -> None:
        balance = self.db_manager_obj.check_balance(user_obj.acc_obj.acc_id)
        if balance[0]>amount:
            if self.db_manager_obj.check_accountid(to_account_id):
                self.db_manager_obj.transfer_query(amount, user_obj.acc_obj.acc_id, to_account_id)
            else:
                print("Destination account doesn't exist")
        else:
            print('Insufficient Funds')

    def display_balance(self ,user_obj:object) -> None:
        res=self.db_manager_obj.check_balance_query(user_obj.user_id)
        print(res)

class UserManager(ModelManager):
    def __init__(self, db_manager_obj) -> None:
        super().__init__(db_manager_obj,'users',User)

    def register(self, username:str, password:str) -> None:
        if not self.db_manager_obj.check_username(username):
            #TODO:i have to validate this username and password first (write a validation module)
            self.db_manager_obj.insert_user(username,password)
        else:
            print('This username already exists try again!!!')

    def login(self, username:str, password:str) -> object:
        res=self.db_manager_obj.login_query(username, password)
        if res:
            if res[0] and res[1]:
                                                                    ## if logged in user already has created account
                bank_obj=BankAccount(int(res[1][1]), res[1][2], int(res[1][3]), int(res[1][0])) 
                return User(res[0][0], res[0][1], res[0][2], bank_obj)
            else:
                return User(res[0][0], res[0][1], res[0][2])
        else:
            return None      

class LogManager:
    def __init__(self) -> None:
        pass

    def clear_log_file(self):
        pass
    
    def transfer_file_to_db(self):
        pass

class DataBaseManager:

    def __init__(self, db_connection_obj:object) -> None:
        self.db_connection_obj=db_connection_obj

    #TODO: try to reduce the with statement with this method
    def execute_queries(self, **kwargs):
        pass

    def insert_user(self, username:str, password:int) -> None:
        query="Insert Into users (username,password) Values (%s,%s)"
        params=(username,password)
        with self.db_connection_obj as db:
            db.cursor.execute(query,params)

    def check_id(self, user_id:int) -> bool:
        query = " Select user_id From users Where user_id=%s;"
        params = (user_id,) 
        with self.db_connection_obj as db:
            db.cursor.execute(query,params)
            result=db.cursor.fetchone()
        if result:
            return True
        else:
          return False 
    
    def check_username(self, username:str) -> bool:
        query = " Select username From users where username=%s";
        params = (username,) 
        with self.db_connection_obj as db:
            db.cursor.execute(query,params)
            result=db.cursor.fetchone()
        if result:    
            return True
        else:
            return False 
    
    def login_query(self, username:str, password:str) -> tuple:
            query = "Select * From users Where username=%s And password=%s"
            param = (username,password)
            query2 = """Select * From accounts Where user_id = %s"""
            with self.db_connection_obj  as db:
                                                        ## To fetch user details
                db.cursor.execute(query,param)
                result = db.cursor.fetchone()
                                                        ## To fetch account details
                param2 = (result[0],)
                db.cursor.execute(query2,param2)
                result2 = db.cursor.fetchone()
            return result,result2 
    
    def insert_account(self, user_id:int, account_type:int, balance:int):
        query="Insert Into accounts (user_id, account_type,balance) values(%s, %s, %s)"
        params=(user_id, account_type, balance)
        with self.db_connection_obj as db:
            db.cursor.execute(query, params)

    def check_accountid(self, account_id:int) -> bool:
        query=f"Select * from accounts Where account_id='{account_id}'"
        with self.db_connection_obj as db:
            db.cursor.execute(query)
            result=db.cursor.fetchone()
        if result:    
            return True
        else:
            return False 

    def check_userid_account(self, user_id:int) -> bool:    
        query=f"Select * From accounts Where user_id='{user_id}'"
        with self.db_connection_obj as db:
            db.cursor.execute(query)
            result=db.cursor.fetchone()
        if result:    
            return True
        else:
            return False 
    
    def check_balance(self, account_id:int) -> tuple:
        query="Select balance from accounts Where account_id=%s"
        params=(account_id,)
        with self.db_connection_obj as db:
            db.cursor.execute(query,params)
            res=db.cursor.fetchone()
        if res:
            return res
        else:
            return None

    def deposit(self, account_id:int, amount:int) -> None:
        query=f"Update accounts Set balance = balance + {amount} Where account_id = '{account_id}'"
        query2=f"Insert Into transactions(account_id,amount,transaction_type,timestamp) Values('{account_id}',{amount},'deposit',CURRENT_TIMESTAMP)"
        # query3 = f"Insert Into logs(message,timestamp,transaction_type,amount) values ('{amount} $ deposited',DEFAULT,'deposit',{amount})"
        with self.db_connection_obj as db:
            db.cursor.execute(query)
            db.cursor.execute(query2)
            # db.cursor.execute(query3)

    def withdraw(self, account_id:int, amount:int) -> None:
        query = f"Update accounts Set balance = balance - {amount} Where account_id = '{account_id}'"
        query2 = f"Insert Into transactions(account_id,amount,transaction_type,timestamp) Values('{account_id}',{amount},'withdrawal',CURRENT_TIMESTAMP)"
        # query3 = f"Insert Into logs(message,timestamp,transaction_type,amount) values ('{amount} $ withdrawed',DEFAULT,'withdraw',{amount})"
        with self.db_connection_obj as db:
            db.cursor.execute(query)
            db.cursor.execute(query2)
            # db.cursor.execute(query3)

    # TODO:write a transfer method
    def transfer_query(self, amount:int, from_account_id:int, to_account_id:int):
        query_des_acc = "Update accounts Set balance=balance+%s where account_id=%s"
        query_org_acc = "Update accounts Set balance=balance-%s where account_id=%s"
        param1 = (amount, to_account_id)
        param2 = (amount, from_account_id)
        with self.db_connection_obj as db:
            db.cursor.execute(query_des_acc,param1)
            db.cursor.execute(query_org_acc,param2)
    
    def transaction_filter(self,**kwargs) -> tuple:
        base_query = f"select * from transactions where"
        conditional_query = " and ".join([f"{key} = %s" for key in kwargs.keys()])
        query = base_query + conditional_query
        params = tuple(kwargs.values())
        with self.db_connection_obj as db:        
            db.cursor.execute(query, params)
            res = db.cursor.fetchall()
            return res
    
    def transactions_above_500(self, account_id:int):
        query="SELECT * FROM transactions WHERE account_id=%s AND ((transaction_type='deposit' AND amount>500) OR (transaction_type='transfer' AND amount>500))"
        params = (account_id,)
        with self.db_connection_obj as db:        
            db.cursor.execute(query, params)
            res = db.cursor.fetchall()
            return res
    
    def insert_log_to_db(self):
        query="insert into log (message, timestamp, transaction_type, amount) values(%s, %s, %s, %s)"
        log_list=[]
        with open("Logs/transaction.log", 'r') as file:
            rows=file.readlines()
            for data in rows:
                log_list.append(tuple(data.strip('\n').split(" - ")))
                
        with self.db_connection_obj as db:
            for data in log_list:
                params=(data[3], data[0], data[1], data[3].split(' ')[0])
                db.cursor.execute(query, params)


DataBaseManager.insert_log_to_db()        