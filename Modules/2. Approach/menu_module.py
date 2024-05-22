from usermanagement import UserManager
from accountmanagement import AccountManager

import os
import time
class Menu:
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
        username=input("Enter your username:")
        password=input("Enter your password:")
        UserManager().register(username,password)
        self.run()
        
    def log_in(self) -> None :
        """This method shows all stored events"""
        username=input("Enter your username:")
        password=input("Enter your password:")
        user_obj=UserManager().login(username,password)
        if user_obj:
            print(f"Welcome {username}.")
            time.sleep(3)
            LoggedInMenu(user_obj).run()    
        else:        
            print('Entered username and password are incorrect')
            time.sleep(3)    
        
    def quit(self) -> None:
        print("See you soon :)",end='')
        return None  

class LoggedInMenu(Menu):
    # Add more options as needed
    def __init__(self, user_obj:object) -> None:
        super().__init__("Manager Menu")
        self.user_obj=None
        self.add_option(1, self.create_account)
        self.add_option(2, self.deposit)
        self.add_option(3, self.withdraw)
        self.add_option(4, self.back_to_main_menu)

    def create_account(self) -> None:
        """This method helps manager to create a events."""
        balance=int(input('Enter user balance:'))
        AccountManager().create_account(self.user_obj,balance)
        self.run()
        
    def deposit(self) -> None:
        """This method edits the manager username and password."""
        amount=int(input('Enter the amount of deposit:'))
        AccountManager().deposit(self.user_obj,amount)
        self.run()

    def withdraw(self) -> None:
        amount=int(input('Enter the amount of withdraw:'))
        AccountManager().withdraw(self.user_obj,amount)        
        self.run()
                  
    def back_to_main_menu(self) -> None:
        """With this method program goes back to the mainmenu."""
        MainMenu().run()  