FROM mysql:8.0

COPY traveltours.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
