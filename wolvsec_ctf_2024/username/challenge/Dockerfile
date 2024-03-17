FROM python:3.12.2
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ .

ENV FLAG=wctf{cr4ck1n_4nd_1nclud1n_4_th3_w1n_1352234}
ENV JWT_SECRET=mstzt

ENV FLAGUSER_PASSWORD=qqz3
RUN useradd -p `openssl passwd -1 -salt hack $FLAGUSER_PASSWORD` -ms /bin/bash flaguser

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]
