import socket
import hashlib
import json
import logging
import asyncio
from sendcheckASY import *
import threading

SALT = 'memkekazazaaafflolol'.encode("utf-8")  # соль для хеширования
varcom = ['logs', 'stop', 'logsclr', 'nameclr']  # Список доступных команд
users = []

# Настройки логгинга (( Взято у умного соседа))
logging.basicConfig(filename="log_serv", level=logging.INFO)

with open('names.json', 'r') as file:
    names = json.load(file)


# def serv_work():  # Сделать!!!
#     print('Сервер работает.')
#     print('Список доступных комманд:')
#     print(varcom)
#     main = True
#     while main:
#         command = input()
#         if command not in varcom:
#             print('Нет такой команды.')
#         elif 'logs' == command:
#             with open('log_serv', 'r') as file:
#                 for raw in file:
#                     print(raw)
#         elif 'logclr' == command:
#             with open('log_serv', 'w') as file:
#                 pass
#         elif 'nameclr' == command:
#             with open('names.json', 'w') as file:
#                 pass
#         elif 'stop' == command:
#             main = False

def hashpass(passw: str):  # Функция хеширования данных
    return hashlib.sha512(passw.encode("utf-8") + SALT).hexdigest()


async def main(HOST, PORT):
    server = await asyncio.start_server(listen, HOST, PORT)
    await server.serve_forever()


def mem(name):  # Функция проверки ip адреса в базе
        if name not in names:
            return False
        else:
            return name


def autoriz(name, passw):  # Функция проверки пароля
    if names[name] == hashpass(passw):
        return True
    else:
        return False


async def listen(reader, writer):
    global users
    autor = False
    addr = writer.get_extra_info('peername')
    logging.info(f"Connect - {addr}")
    senduser(writer, 'Добро пожаловать! Введите Логин: ')
    login = await checkmsg(reader)
    check = mem(login)
    if check:
        while not autor:
            senduser(writer, f'Здравствуйте, {login}, Введите пароль: ')
            passw = await checkmsg(reader) 
            autor = autoriz(login, passw)
    else:
        senduser(writer, f'Регистрация нового пользователя, {login}, Введите пароль:  ')
        passw = await checkmsg(reader)
        names[login] = hashpass(passw)
        with open('names.json', 'w') as file:
            json.dump(names, file)
        autor = True         
    users.append(writer)
    senduser(writer, 'Здесь сегодня тесновато. Но для тебя всегда место найдется!')
    
    while autor:
        msg = await checkmsg(reader)
        if msg:
            sendmsg(users, login+': '+msg)
        










port = 9090
portmiss = True
adress = ['localhost', '192.168.0.101']


asyncio.run(main(adress[0], port))