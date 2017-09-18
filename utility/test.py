from django.core.mail import send_mail


def main():
    send_mail('盛世润达注册', 'ok，可以行得通???', 'drinksober@foxmail.com', ['drinks.huang@hypers.com'])
