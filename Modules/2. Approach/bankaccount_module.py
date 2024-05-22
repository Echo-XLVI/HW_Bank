import uuid

class BankAccount:
    def __init__(self , user_id:str, balance:int, acc_id:str=None) -> None:
        self.acc_id=acc_id
        self.user_id=user_id
        self.balance=balance
