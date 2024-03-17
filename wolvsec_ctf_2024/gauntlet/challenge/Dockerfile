FROM python:3.12.2
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ .

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]
