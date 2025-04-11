

import json
import socket
import tkinter as tk

from utilities.center_windows import center_window
from pages.login import login
from pages.register import register

IP = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.settimeout(3)

root = tk.Tk()
center_window(root, 400, 300)
root.title("Welcome")


def exit_app():
    json_output = json.dumps({"data": "", "action": "BYE"})
    client.send(json_output.encode())
    response = client.recv(1024).decode()
    root.destroy()
    client.close()

button_width = 30
button_pad_y = 10
tk.Button(root, text="Регистрация", width=button_width, command=lambda : register(root, client)).pack(pady=button_pad_y)
tk.Button(root, text="Логин",  width=button_width, command=lambda : login(root, client)).pack(pady=button_pad_y)
tk.Button(root, text="Выход",  width=button_width, command=exit_app).pack(pady=(button_pad_y, 20))

root.mainloop()

