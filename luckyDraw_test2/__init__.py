import pymysql
import django_crontab

pymysql.install_as_MySQLdb()


def my_callback(sender, **kwargs):
    print("my_callback")
    print(sender, kwargs)

