DROP USER IF EXISTS 'employee_user'@'localhost';
CREATE USER 'user_user'@'localhost' IDENTIFIED BY 'Aauth123';

DROP DATABASE IF EXISTS employee;
CREATE DATABASE IF EXISTS employee;

GRANT ALL PRIVILEGES ON employee.* TO 'employee_user'@'localhost';
FLUSH PRIVILEGES;

USE employee;

DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    surname VARCHAR(60) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    standard_rate DECIMAL(8,2) NOT NULL,
    hours_worked DECIMAL(8,2) NOT NULL,
    overtime_rate DECIMAL(8,2) NOT NULL,
    overtime_hours DECIMAL(8,2) NOT NULL,
    contract ENUM('full time', 'part time', 'contractor') NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO employee (first_name, surname, email, standard_rate, hours_worked, overtime_rate, overtime_hours, contract, password)
VALUES ('test', 'employee', 'test@employee.com', 10, 40, 15, 0, 'full time', 'testpass');