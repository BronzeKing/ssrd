#!/bin/sh
pypy3 manage.py migrate
pypy3 manage.py runserver_plus 0.0.0.0:8888
