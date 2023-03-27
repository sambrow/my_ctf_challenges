FROM node:12
# install xmllint (an command-line XML parser)
RUN apt-get update && apt-get install -y libxml2-utils
RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./ ./
RUN npm install
EXPOSE 12345

CMD ["node", "server.js"]
