CREATE DATABASE db_logins;
USE db_logins;

CREATE TABLE [Clients]
(
    [ID] INT IDENTITY,
	[Time_log] VARCHAR(50),
    [login] VARCHAR(50) NOT NULL UNIQUE,
	[Name] VARCHAR(50) NOT NULL,
    [Password] VARCHAR(255) NOT NULL,
	[Sex] VARCHAR(20) NOT NULL,
	[Age] INT NOT NULL,
	[Ves] FLOAT NOT NULL,
	[Rost] FLOAT NOT NULL
);



SELECT * FROM [Clients]
DROP TABLE [Clients]