FROM ubuntu:18.04
# install software
RUN apt update && apt install -y software-properties-common wget xvfb xdotool libgtk-3-0

# download Archi, unzip Archi
RUN wget https://www.archimatetool.com/downloads/4.5.1/Archi-Linux64-4.5.1.tgz && mkdir -p /Archi && tar -xvzf Archi-Linux64-4.5.1.tgz -C /

# copy script 
COPY export-svg.sh /root/export-to-svg.sh

# start virtual display
ENV DISPLAY :20

# !!! IMPORTANT !!! current file expected to have external mapping to "/external" folder
