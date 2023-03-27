FROM node:12
RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./ ./
RUN npm install
EXPOSE 12341

CMD ["node", "server.js"]
