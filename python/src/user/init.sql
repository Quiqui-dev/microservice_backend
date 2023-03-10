-- DROP USER IF EXISTS 'webWrite'@'localhost';
-- CREATE USER 'webWrite'@'localhost' IDENTIFIED BY 'Aauth123';

DROP DATABASE IF EXISTS XT;
CREATE DATABASE XT;

-- GRANT ALL PRIVILEGES ON user.* TO 'webWrite'@'localhost';
-- FLUSH PRIVILEGES;

USE XT;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY NOT NULL,
    username VARCHAR(60) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    date_joined DATETIME NOT NULL
)