import uuid

class BankAccount:
    def __init__(self ,acc_id:str, user_id:str, balance:int) -> None:
        self.acc_id=acc_id
        self.user_id=user_id
        self.balance=balance
