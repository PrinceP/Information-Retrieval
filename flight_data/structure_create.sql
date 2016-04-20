/*
creating database
*/

CREATE DATABASE IF NOT EXISTS IR_PROJECT;

USE IR_PROJECT;

/*
creting table flights
*/
CREATE TABLE IF NOT EXISTS flights(
id int PRIMARY KEY AUTO_INCREMENT,
operator varchar(255) NOT NULL,
operatorcode varchar(255) NOT NULL,
flightno varchar(255) NOT NULL,
source varchar(255) NOT NULL,
destination varchar(255) NOT NULL,
departuretime varchar(255) NOT NULL,
arrivaltime varchar(255) NOT NULL,
days varchar(255) NOT NULL,
stop int NOT NULL
);