

import json
import socket
import hashlib
import tkinter as tk
from tkinter import messagebox

from pages.register import register

IP = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

root = tk.Tk()
root.title("Welcome")
root.geometry("300x200")



# def register():
    # reg_window = tk.Toplevel(root)
    # reg_window.title("Регистрация")
    # reg_window.geometry("300x400")
    #
    # tk.Label(reg_window, text="Логин:").pack()
    # login_entry = tk.Entry(reg_window)
    # login_entry.pack()
    #
    # tk.Label(reg_window, text="Введите вашe имя:").pack()
    # name_entry = tk.Entry(reg_window)
    # name_entry.pack()
    #
    # tk.Label(reg_window, text = "Введите ваш пол:").pack()
    # sex_entry = tk.Entry(reg_window)
    # sex_entry.pack()
    #
    # tk.Label(reg_window, text="Введите ваш возраст:").pack()
    # age_entry = tk.Entry(reg_window)
    # age_entry.pack()
    #
    # tk.Label(reg_window, text="Введите ваш вес:").pack()
    # ves_entry = tk.Entry(reg_window)
    # ves_entry.pack()
    #
    # tk.Label(reg_window, text="Введите ваш рост:").pack()
    # rost_entry = tk.Entry(reg_window)
    # rost_entry.pack()
    #
    # tk.Label(reg_window, text="Пароль:").pack()
    # password_entry = tk.Entry(reg_window, show="*")
    # password_entry.pack()
    #
    # tk.Label(reg_window, text="Повторите пароль:").pack()
    # password_confirm_entry = tk.Entry(reg_window, show="*")
    # password_confirm_entry.pack()
    #
    #
    # def send_register():
    #     login_name = login_entry.get().strip()
    #     name = name_entry.get()
    #     sex = sex_entry.get().lower()
    #     age = age_entry.get()
    #     ves = ves_entry.get()
    #     rost = rost_entry.get()
    #     password = password_entry.get()
    #     password_confirm = password_confirm_entry.get()
    #
    #     register_data = [login_name, name, sex, age, ves, rost]
    #
    #     for item in register_data:
    #         if not item:
    #             messagebox.showerror("Ошибка", f"Убедитесь что все поля введены")
    #             return
    #
    #     if password != password_confirm or not login_name or not password:
    #         messagebox.showerror("Ошибка", "Пароли не совпадают или пустые поля")
    #         return
    #
    #     hashed_password = hashlib.sha256(password.encode()).hexdigest()
    #     json_output = json.dumps({"data": {"login_name": login_name,
    #                                        "password": hashed_password,
    #                                        "name" : name,
    #                                        "sex" : sex,
    #                                        "age" : age,
    #                                        "ves" : ves,
    #                                        "rost" : rost}, "action": "REGISTER"})
    #
    #     client.send(json_output.encode())
    #     response = client.recv(1024).decode()
    #     messagebox.showinfo("Ответ сервера", response)
    #     reg_window.destroy()
    #
    # tk.Button(reg_window, text="Зарегистрироваться", command=send_register).pack()




def login():
    login_window = tk.Toplevel(root)
    login_window.title("Логин")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Логин:").pack()
    login_entry = tk.Entry(login_window)
    login_entry.pack()

    tk.Label(login_window, text="Пароль:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def send_login():
        login_name = login_entry.get().strip()
        password = password_entry.get()

        if not login_name or not password:
            messagebox.showerror("Ошибка", "Поля не должны быть пустыми")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        json_output = json.dumps({"data": {"login_name": login_name, "password": hashed_password}, "action": "LOGIN"})
        client.send(json_output.encode())

        response = json.loads(client.recv(1024).decode())
        name = response["name"]

        if response["action"] == "IN":
            InAccount(name)

        login_window.destroy()


    tk.Button(login_window, text="Войти", command=send_login).pack()


def InAccount(name):
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


def exit_app():
    json_output = json.dumps({"data": "", "action": "BYE"})
    client.send(json_output.encode())
    response = client.recv(1024).decode()
    root.destroy()
    client.close()

tk.Button(root, text="Регистрация", command=lambda : register(root, client)).pack(pady=5)
tk.Button(root, text="Логин", command=login).pack(pady=5)
tk.Button(root, text="Выход", command=exit_app).pack(pady=5)

root.mainloop()

