FROM debian
RUN apt-get update && apt-get install git-core -y

RUN mkdir server
WORKDIR /server
COPY . /server
WORKDIR  /server/scripts
RUN chmod +x  server-setup.sh
RUN ./server-setup.sh -a
