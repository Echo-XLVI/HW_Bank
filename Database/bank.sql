Create DataBase Bank

Create Table users
(user_id varchar(30) Constraint PK_users_user_id Primary Key,
 username varchar(30) Constraint UQ_users_username not null,
 "password" varchar(16) not null
);

Create Table account
(account_id varchar(30) Constraint PK_account_account_id Primary Key,
 user_id varchar(30) Constraint FK_account_user_id References users(user_id) not null,
 balance int not null
);

Create Table transaction
(transaction_id serial Constraint PK_transaction_transaction_id Primary Key,
 account_id varchar(30) Constraint FK_account_account_id References account(account_id) not null,
 transaction_type varchar(20) not null,
 amount int not null,
"timestamp" timestamp not null
);
--------------------------------------------------
select * from users;
Select * From account;
select * from transaction;
drop table transaction;
drop table account;
drop table users;

update account
set balance=balance - 300;