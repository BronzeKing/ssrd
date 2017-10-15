FROM python:3.5

ENV PYTHONUNBUFFERED 1
RUN sed -i s@archive.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@deb.debian.org@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@security.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list


RUN groupadd -r django \
    && useradd -r -g django django

COPY ./compose/django/gunicorn.sh ./compose/django/entrypoint.sh /
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

COPY . /app

RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com --index-url http://mirrors.aliyun.com/pypi/simple/ -r /requirements/production.txt
RUN chown -R django /app

USER django

WORKDIR /app

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/entrypoint.sh"]
