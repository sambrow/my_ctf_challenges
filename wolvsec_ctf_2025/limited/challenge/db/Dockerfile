FROM mysql:9.0.1

ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=ctf
ENV MYSQL_USER=ctf
ENV MYSQL_PASSWORD=password

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initialize /docker-entrypoint-initdb.d
