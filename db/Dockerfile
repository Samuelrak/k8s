FROM mariadb:latest

RUN mkdir /data

COPY traveltours.sql /docker-entrypoint-initdb.d/

COPY my.cnf /etc/mysql/my.cnf

RUN chmod 777 /docker-entrypoint-initdb.d/traveltours.sql

