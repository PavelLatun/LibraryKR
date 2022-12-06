CREATE DATABASE IF NOT EXISTS library;

CREATE TABLE IF NOT EXISTS library.books (
    ID int NOT NULL AUTO_INCREMENT,
    title text,
    year int,
    author text,
    PRIMARY KEY (ID)
);