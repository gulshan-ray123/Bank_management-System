Create database if not exists
CREATE DATABASE IF NOT EXISTS bank;

Use the database
USE bank;

-- Customers table
CREATE TABLE IF NOT EXISTS cust_detail (
    AccountNo INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Contact BIGINT NOT NULL,
    Address VARCHAR(100) NOT NULL,
    Aadhar VARCHAR(12) NOT NULL,
    PIN VARCHAR(20) NOT NULL
);

-- Managers table
CREATE TABLE IF NOT EXISTS managers (
    ManagerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Username VARCHAR(50) NOT NULL,
    PIN VARCHAR(20) NOT NULL
);

-- Cashiers table
CREATE TABLE IF NOT EXISTS cashiers (
    CashierID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Username VARCHAR(50) NOT NULL,
    PIN VARCHAR(20) NOT NULL
);

-- Loans table
CREATE TABLE IF NOT EXISTS loans (
    LoanID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    LoanAmount DECIMAL(20, 2) NOT NULL,
    Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (CustomerID) REFERENCES cust_detail(AccountNo)
);
 insert into managers(FirstName, LastName,Username,PIN) values("Gulshan","Ray","manager", "manager_password");
insert into cashiers(FirstName,LastName,UserName,PIN) values("Lav","Raj","cashier", "cashier_password");
select * from cust_detail;
