FROM node:latest
RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install
COPY ./app.js ./
COPY ./flag.txt ./
EXPOSE 8000

CMD ["node", "app.js"]
