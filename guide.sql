CREATE DATABASE arduino;

CREATE TABLE tbl_user (
  user_name VARCHAR(20) NOT NULL,
  user_password VARCHAR(20) NOT NULL,
  PRIMARY KEY (user_name)
  );

CREATE TABLE board (
  id tag(11) unsigned NOT NULL auto_increment,
  LOG VARCHAR(20) NULL,
  NAME VARCHAR(20) NULL,
  TIME VARCHAR(20) NULL,
  ID VARCHAR(20) NULL,
  PRIMARY KEY (tag)
  );

ALTER TABLE board ADD UNIQUE INDEX (TIME);
