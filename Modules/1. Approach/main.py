from usermanagement import UserManager
from accountmanagement import AccountManager
from log_module import Log

import os
import time

user_obj=None

def login_inner_menu():
    while True:
        os.system('cls')
        op=int(input('1.Create account\n2.deposit\n3.Withdraw\n4.log out\nChoose your operation:'))
        match op:
            case 1:
                balance=int(input('Enter user balance:'))
                AccountManager().create_account(user_obj,balance)
                Log.log_info('create account','account created')
            case 2:
                amount=int(input('Enter the amount of deposit:'))
                AccountManager().deposit(user_obj,amount)
                Log.log_info('deposit','deposit transfered')
            case 3:
                amount=int(input('Enter the amount of withdraw:'))
                AccountManager().withdraw(user_obj,amount)
                Log.log_info('withdraw',f'{amount} withdrawed')
            case 4:
                Log.log_info('login',f'{user_obj.username} logged out')
                break
            case __:
                print('Enterd operation is wrong!!!')
                time.sleep(3)

def login_menu():    
    os.system('cls')
    username=input("Enter your username:")
    password=input("Enter your password:")
    res=UserManager().login(username,password)
    if res:
        Log.log_info('login',f'{username} logged in')
        print(f"Welcome {username}.")
        time.sleep(3)
        global user_obj
        user_obj=res
        login_inner_menu()
    else:        
        print('Entered username and password are incorrect')
        time.sleep(3)

def register_menu():
    username=input("Enter your username:")
    password=input("Enter your password:")
    UserManager().register(username,password)
    Log.log_info('register',f'{username} registered')

def main_menu():
    ex=False
    while True:
        os.system('cls')
        op=int(input("1.Register\n2.Login\n3.Exit\nEnter your operation:"))
        match op:
            case 1:
                register_menu()
            case 2:
                login_menu()
            case 3:                
                ex=True
            case __:
                print('Enterd operation is wrong!!!')
                time.sleep(3)
        if ex==True:
            break

if __name__=="__main__":
    main_menu()