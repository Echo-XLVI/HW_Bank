from bankaccount_module import BankAccount
from databasemanagement import DataBaseManager as dbm
import uuid
class AccountManager:
    def __init__(self) -> None:
        pass

    def create_account(self, user_obj:object, balance:int):
        while True:
            if not dbm.check_userid_account(user_obj.user_id):
                account_id=''.join(str(uuid.uuid4()).split('-'))[:30]
                if not dbm.check_accountid(account_id):
                    acc_obj=BankAccount(account_id, user_obj.user_id, balance)
                    user_obj.acc_obj=acc_obj
                    dbm.insert_account(user_obj.user_id, account_id, balance)
                    break
            else:
                print("You've already created an acoount!!!")

    def deposit(self, user_obj:object, amount:int):
        dbm.deposit(user_obj.acc_obj.acc_id, amount)

    def withdraw(self, user_obj:object, amount:int):
        balance=int(dbm.check_balance(user_obj.acc_obj.acc_id)[0])
        if balance>amount:
            dbm.withdraw(user_obj.acc_obj.acc_id, amount)
        else:
            print('Insufficient Funds')
