FROM postgres:9.6

RUN sed -i s@archive.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@deb.debian.org@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@security.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list

# add backup scripts
ADD backup.sh /usr/local/bin/backup
ADD restore.sh /usr/local/bin/restore
ADD list-backups.sh /usr/local/bin/list-backups

# make them executable
RUN chmod +x /usr/local/bin/restore
RUN chmod +x /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/backup
