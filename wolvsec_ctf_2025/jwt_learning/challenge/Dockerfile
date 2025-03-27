FROM node:latest

RUN mkdir -p /ctf/app
WORKDIR /ctf/app

COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY ./index.js ./
COPY ./public/ ./public/

EXPOSE 3000

CMD ["node", "index.js"]
