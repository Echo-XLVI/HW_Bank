from manager_module import AccountManager,UserManager,DataBaseManager
from log_module import Log
from databaseconnection import DataBaseConnection
import os
import time
class Menu:
    db_connection_obj = DataBaseConnection()
    db_manager_obj = DataBaseManager(db_connection_obj)
    user_manager_obj = UserManager(db_manager_obj)
    acc_manager_obj = AccountManager(db_manager_obj)
    log_obj = Log()

    def __init__(self, name:str) -> None:
        self.name = name
        self.options = {}  # Map option numbers to actions

    def add_option(self, option_number:int, action:object) -> None:
        """This method is kinda a setter for 'options' attribute in the Menu class."""
        self.options[option_number] = action

    def display(self) -> None:
        """This method just display the instantiated menu by it's attributes which is its options and its name."""
        print(f"{self.name:=^30}")
        for option_number, action in self.options.items():
            print(f"{option_number}. {action.__name__}")

    def run(self) -> None:  
        """This method is the initiate point of the Menu module
            it will show the subclasses options and user can choose
            then the executive code within the selected option will run.""" 
        os.system('cls')   
        self.display()
        choice = int(input("Enter your choice:"))
        if choice in self.options.keys():
            self.options[choice]()  # Call the action function
        else:
            print("Invalid choice. Please try again.")

class MainMenu(Menu):
    # Add more options as needed
    def __init__(self) -> None:
        super().__init__("Main Menu")
        self.add_option(1, self.register)
        self.add_option(2, self.log_in)
        self.add_option(3, self.quit)

    def register(self) -> None:
        """This method goes to the manager menu base on validation of the username and password user gaves."""
        try:    
            username=input("Enter your username:")
            password=input("Enter your password:")
            self.user_manager_obj.register(username,password)
            self.log_obj.log('register',f"Account with username : {username} registered",'DEBUG')
        except Exception as e:
            self.log_obj.log(f'{Exception.__class__}',e,'INFO','error','a')        
            self.log_obj.log(f'{Exception.__class__}',e ,'ERROR')
        finally:    
            self.run()  
        
    def log_in(self) -> None :
        """This method shows all stored events"""
        try:
            username=input("Enter your username:")
            password=input("Enter your password:")
            user_obj=self.user_manager_obj.login(username,password)
            if user_obj:
                print(f"Welcome {username}.")
                time.sleep(3)
                self.log_obj.log('log in',f"Account with id : {user_obj.user_id} logged in",'DEBUG')
                LoggedInMenu(user_obj).run()    
            else:        
                print('Entered username and password are incorrect')
                time.sleep(3)
        except Exception as e:
            self.log_obj.log(f'{Exception.__class__}',e,'INFO','error','a')        
            self.log_obj.log(f'{Exception.__class__}',e ,'ERROR')
            self.run()  
        
    def quit(self) -> None:
        print("See you soon :)",end='')
        return None  

class LoggedInMenu(Menu):
    

    # Add more options as needed
    def __init__(self, user_obj:object) -> None:
        super().__init__("Manager Menu")
        self.user_obj = user_obj
        self.add_option(1, self.create_account)
        self.add_option(2, self.deposit)
        self.add_option(3, self.withdraw)
        self.add_option(4, self.transfer)
        self.add_option(5, self.back_to_main_menu)

    def create_account(self) -> None:
        """This method helps manager to create a events."""
        try:    
            balance = int(input('Enter user balance:'))
            acc_type = input("Enter your account type:") 
            self.acc_manager_obj.create_account(self.user_obj,acc_type,balance)
            self.log_obj.log('create account',f'Account id:{self.user_obj.user_id} created','DEBUG') 
        except Exception as e:
            self.log_obj.log(f'{Exception.__class__}',e,'INFO','error','a')        
            self.log_obj.log(f'{Exception.__class__}',e ,'ERROR')
        finally:
            self.run() 
        
    def deposit(self) -> None:
        """This method edits the manager username and password."""
        try:
            amount=int(input('Enter the amount of deposit:'))
            self.acc_manager_obj.deposit(self.user_obj,amount)
            self.log_obj.log('deposit',f'{amount} deposited','INFO','transaction','a')        
            self.log_obj.log('deposit',f'{amount} deposited','DEBUG')  
            self.run() 
        except Exception as e:
            self.log_obj.log(f'{Exception.__class__}',e,'INFO','error','a')        
            self.log_obj.log(f'{Exception.__class__}',e ,'ERROR')
        finally:
            self.run() 

    def withdraw(self) -> None:
        try:
            amount=int(input('Enter the amount of withdraw:'))
            self.acc_manager_obj.withdraw(self.user_obj,amount)   
            self.log_obj.log('withdraw',f'{amount} withdrawed','INFO','transaction','a')        
            self.log_obj.log('withdraw',f'{amount} withdrawed','DEBUG')         
            self.run() 
        except Exception as e:
            self.log_obj.log(f'{Exception.__class__}',e,'INFO','error','a')        
            self.log_obj.log(f'{Exception.__class__}',e ,'ERROR')
        finally:
            self.run() 

    def transfer(self) -> None:
        try:
            to_account=int(input('Enter destination account id:'))
            amount=int(input('Enter the amount to transfer:'))
            self.acc_manager_obj.transfer(self.user_obj,to_account,amount)
            self.log_obj.log('transfer',f'{amount} transfered','INFO','transaction','a')        
            self.log_obj.log('transfer',f'{amount} transfered','DEBUG') 
        except Exception as e:
            self.log_obj.log(f'{Exception.__class__}',e,'INFO','error','a')        
            self.log_obj.log(f'{Exception.__class__}',e ,'ERROR')
        finally:
            self.run() 

    def display_balance(self) -> None:
        self.user_obj.acc_obj.display_balance(self.user_obj)
        time.sleep(3)
        self.run()

    def back_to_main_menu(self) -> None:
        """With this method program goes back to the mainmenu."""
        MainMenu().run()  