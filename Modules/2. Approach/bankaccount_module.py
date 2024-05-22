import uuid

class BankAccount:

    def __init__(self , user_id:str, account_type:str, balance:int, acc_id:str=None) -> None:
        self.acc_id=acc_id
        self.user_id=user_id
        self.account_type=account_type
        self.balance=balance
