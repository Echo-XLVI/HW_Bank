from databasemanagement import DataBaseManager as dbm
from user import User
from bankaccount_module import BankAccount

import uuid

class UserManager:
    def __init__(self) -> None:
        pass

    def register(self, username:str, password:str) -> None:
        if not dbm.check_username(username):
            while (True):
                user_id=''.join(str(uuid.uuid4()).split('-'))[:30]
                if not dbm.check_id(user_id):
                    User(user_id,username,password)
                    dbm.insert_user(user_id,username,password)
                    break
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

######################################### Test
# print(''.join(str(uuid.uuid4()).split('-'))[:30])
# UserManager().register('reza','1380ACreza')
# UserManager().login('echo','1234')