CREATE DATABASE churn_db;
USE churn_db;
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    RowNumber INT,
    CustomerId INT,
    Surname VARCHAR(100),
    CreditScore INT,
    Geography VARCHAR(50),
    Gender VARCHAR(20),
    Age INT,
    Tenure INT,
    Balance DECIMAL(15, 2),
    NumOfProducts INT,
    HasCrCard INT,
    IsActiveMember INT,
    EstimatedSalary DECIMAL(15, 2),
    Exited INT );
    SELECT * FROM customers LIMIT 10;
    SELECT COUNT(*) FROM customers;