FROM ubuntu
RUN apt update
RUN apt install xterm vim wget sudo -y
RUN sudo useradd --create-home user
RUN echo "user:clone"|chpasswd 
RUN sudo usermod -aG sudo user
RUN su - user