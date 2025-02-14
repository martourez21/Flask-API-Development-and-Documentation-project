DROP DATABASE IF EXISTS trivia;
DROP USER IF EXISTS postgres;
CREATE DATABASE trivia;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE trivia TO postgres;
ALTER USER postgres CREATEDB;
ALTER USER postgres WITH SUPERUSER;