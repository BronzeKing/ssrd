FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf


RUN sed -i s@archive.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@deb.debian.org@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@security.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list

# installs the `ps` command in the nginx image
RUN apt-get update && apt-get install -y procps

ADD start.sh /start.sh
ADD nginx-secure.conf /etc/nginx/nginx-secure.conf
ADD dhparams.pem /etc/ssl/private/dhparams.pem
CMD /start.sh

