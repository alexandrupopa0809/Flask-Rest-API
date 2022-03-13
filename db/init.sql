CREATE DATABASE meteo;
use meteo;

CREATE TABLE tari (
    id INT NOT NULL AUTO_INCREMENT,
    nume_tara VARCHAR(200) UNIQUE,
    lat DOUBLE,
    lon DOUBLE,
    PRIMARY KEY (id)
);

CREATE TABLE orase (
    id INT NOT NULL AUTO_INCREMENT,
    id_tara INT,
    nume_oras VARCHAR(200),
    lat DOUBLE,
    lon DOUBLE,
    PRIMARY KEY (id),
    CONSTRAINT UC_tara UNIQUE (id_tara, nume_oras),
    CONSTRAINT FK_tara FOREIGN KEY (id_tara) REFERENCES tari(id) on delete cascade
);

CREATE TABLE temperaturi (
    id INT NOT NULL AUTO_INCREMENT,
    valoare DOUBLE,
    timestamp DATE,
    id_oras INT,
    PRIMARY KEY(id),
    CONSTRAINT UC_oras UNIQUE (id_oras, timestamp),
    CONSTRAINT FK_oras FOREIGN KEY (id_oras) REFERENCES orase(id) on delete cascade
);
