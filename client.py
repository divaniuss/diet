

import json
import socket
import hashlib
import tkinter as tk
from tkinter import messagebox

from pages.login import login
from pages.register import register

IP = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.settimeout(3)

root = tk.Tk()
root.title("Welcome")
root.geometry("300x200")


# как спавнить окно ПО ЦЕНТРУ БЛЯТЬ
# зарефакторить InAcc и сервер


def exit_app():
    json_output = json.dumps({"data": "", "action": "BYE"})
    client.send(json_output.encode())
    response = client.recv(1024).decode()
    root.destroy()
    client.close()

tk.Button(root, text="Регистрация", command=lambda : register(root, client)).pack(pady=5)
tk.Button(root, text="Логин", command=lambda : login(root, client)).pack(pady=5)
tk.Button(root, text="Выход", command=exit_app).pack(pady=5)

root.mainloop()

