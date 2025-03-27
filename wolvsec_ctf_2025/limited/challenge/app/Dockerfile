FROM python:3.11.3-bullseye
#RUN apt-get update && apt-get upgrade -y && apt-get install -y default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

ENV MYSQL_DB=ctf
ENV MYSQL_USER=ctf
ENV MYSQL_PASSWORD=password

RUN mkdir /app
WORKDIR /app
RUN useradd -M -d /app ctf

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .

RUN chown -R root:ctf /app 
RUN chmod -R 750 /app

USER ctf

CMD ["python3", "-u", "/app/app.py"]