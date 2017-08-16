# encoding: utf-8

from django.core.mail import send_mail


def main():
    send_mail('测试一下吧', '可以行得通???', 'drinksober@foxmail.com', ['drinks.huang@hypers.com'])
