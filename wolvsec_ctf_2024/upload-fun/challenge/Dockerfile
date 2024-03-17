FROM php:8.3.1-apache-bullseye

RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd -r ctf && useradd -r -g ctf ctf

RUN chmod -R 755 /etc/apache2 &&\
    chmod -R 755 /var/www/

COPY flag.txt /flag.txt
RUN chown admin:admin /flag.txt && chmod 444 /flag.txt

COPY src /var/www/html

RUN chown -R root:root /var/www/html &&\
    chmod -R 555 /var/www/html

RUN mkdir -p /var/www/html/uploads && chmod -R 333 /var/www/html/uploads

RUN rm -f /bin/chmod /usr/bin/chmod /bin/chown /usr/bin/chown /usr/bin/curl usr/bin/apt-get

USER ctf

EXPOSE 80
