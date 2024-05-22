Create DataBase Bank

Create Table users
(user_id serial Constraint PK_users_user_id Primary Key,
 username varchar(30) Constraint UQ_users_username not null,
 "password" varchar(16) not null
);

Create Table accounts
(account_id serial Constraint PK_account_account_id Primary Key,
 user_id serial Constraint FK_account_user_id References users(user_id) not null,
 account_type varchar(20) not null,
 balance int not null
);

Create Table transactions
(transaction_id serial Constraint PK_transaction_transaction_id Primary Key,
 account_id serial Constraint FK_account_account_id References account(account_id) not null,
 transaction_type varchar(20) not null,
 amount int not null,
"timestamp" timestamp not null
);

Create Table Logs
(
);
--------------------------------------------------
select * from users;
Select * From accounts;
select * from transactions;
drop table transactions;
drop table account;
drop table users;

update account
set balance=balance - 300;