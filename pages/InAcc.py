import json
import socket
import tkinter as tk
from tkinter import messagebox

def InAccount(name, root, client):
    login_in_window = tk.Toplevel(root)
    login_in_window.title(f"Добро пожаловать {name}")
    login_in_window.geometry("350x300")

    def AddFood():
        return

    def AllFood():
        return

    def Goal():
        return

    def Exit():
        login_in_window.destroy()

    button_width = 30
    button_pad_y = 10
    tk.Button(login_in_window, text="Добавить новую еду", width=button_width, command=AddFood).pack(pady=button_pad_y)
    tk.Button(login_in_window, text="Посмотреть, что вы сегодня съели", width=button_width, command=AllFood).pack(pady=button_pad_y)
    tk.Button(login_in_window, text="Посмотреть цель калорий на день", width=button_width, command=Goal).pack(pady=button_pad_y)
    tk.Button(login_in_window, text="Выйти",width=button_width, command=Exit).pack(pady=(button_pad_y, 20))