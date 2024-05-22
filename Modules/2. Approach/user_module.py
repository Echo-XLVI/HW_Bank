import re

class User:
    def __init__(self, user_id:str, username:str, password:str, acc_obj:object=None) -> None:
        self.user_id=user_id
        self.username=username
        self.__password=password
        self.acc_obj=acc_obj
    
    @property
    def password(self) -> str:
        return self.password
    
    @password.setter
    def password(self, password:str) -> None:
        assert self.__pass_validation(password),'Entered password is invalid'
        self.__password=password

    @staticmethod
    def __pass_validation(password:str) -> bool:
        return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",password)
