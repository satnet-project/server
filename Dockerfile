FROM debian
RUN apt-get update  

#WORKDIR /server/scripts
#ADD server-setup.sh /server-setup.sh
#RUN chmod 0755 /server-setup.sh
# Define default command.
#CMD ["ls"]

#RUN cd /server/scripts
ADD /scripts/server-setup.sh server-setup.sh
RUN chmod 0755  server-setup.sh
RUN pwd
RUN ls
RUN /server-setup.sh -a
#RUN cd /home ; ls
