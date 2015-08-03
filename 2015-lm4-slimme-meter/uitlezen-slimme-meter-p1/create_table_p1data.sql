-- Table: p1data_old

-- DROP TABLE p1data;

CREATE TABLE p1data
(
  utc_timestamp INTEGER NOT NULL UNIQUE PRIMARY KEY,
  daldag REAL,
  piekdag REAL,
  dalterug REAL,
  piekterug REAL,
  gas REAL,
  afgenomen_vermogen REAL,
  teruggeleverde_vermogen REAL
);

  
