CREATE DATABASE IF NOT EXISTS hospitaldb;
USE hospitaldb;

CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

INSERT INTO hospitals (name, address) VALUES ('Hospital A', 'Address A');
INSERT INTO hospitals (name, address) VALUES ('Hospital B', 'Address B');

