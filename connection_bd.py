# import mysql.connector
import sqlite3


def connect():
    # Подключение к базе данных(Удалённая БД MYSQL)
    # try:
    #     connection = mysql.connector.connect(
    #         host='p548561.ispmgr.mchost.ru',
    #         database='p548561_threatanalys',
    #         # user='p548561_maxim3',
    #         user='p548561_maximalo4ka',
    #         password='maxon4ik.py'
    #     )
    #
    #     if connection.is_connected():
    #         db_Info = connection.get_server_info()
    #         print("Connected to MySQL Server version ", db_Info)
    #         cursor = connection.cursor()
    #
    #         return connection, cursor
    #         # Здесь можно выполнять SQL-запросы
    #
    # except mysql.connector.Error as e:
    #     return ("Error while connecting to MySQL", e)

    # Подключение к базе данных(локальная БД SQLlite)
    try:
        connection = sqlite3.connect('threatanalisys.db')
        cursor = connection.cursor()
        print('Connected')

        return connection, cursor

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
