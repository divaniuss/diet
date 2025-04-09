import json
import socket
import hashlib
import tkinter as tk
from tkinter import messagebox

def register(root, client):
    reg_window = tk.Toplevel(root)
    reg_window.title("Регистрация")
    reg_window.geometry("300x400")

    tk.Label(reg_window, text="Логин:").pack()
    login_entry = tk.Entry(reg_window)
    login_entry.pack()

    tk.Label(reg_window, text="Введите вашe имя:").pack()
    name_entry = tk.Entry(reg_window)
    name_entry.pack()

    tk.Label(reg_window, text = "Введите ваш пол:").pack()
    sex_entry = tk.Entry(reg_window)
    sex_entry.pack()

    tk.Label(reg_window, text="Введите ваш возраст:").pack()
    age_entry = tk.Entry(reg_window)
    age_entry.pack()

    tk.Label(reg_window, text="Введите ваш вес:").pack()
    ves_entry = tk.Entry(reg_window)
    ves_entry.pack()

    tk.Label(reg_window, text="Введите ваш рост:").pack()
    rost_entry = tk.Entry(reg_window)
    rost_entry.pack()

    tk.Label(reg_window, text="Пароль:").pack()
    password_entry = tk.Entry(reg_window, show="*")
    password_entry.pack()

    tk.Label(reg_window, text="Повторите пароль:").pack()
    password_confirm_entry = tk.Entry(reg_window, show="*")
    password_confirm_entry.pack()


    def send_register():
        login_name = login_entry.get().strip()
        name = name_entry.get()
        sex = sex_entry.get().lower()
        age = age_entry.get()
        ves = ves_entry.get()
        rost = rost_entry.get()
        password = password_entry.get()
        password_confirm = password_confirm_entry.get()

        register_data = [login_name, name, sex, age, ves, rost]

        for item in register_data:
            if not item:
                messagebox.showerror("Ошибка", f"Убедитесь что все поля введены")
                return

        if password != password_confirm or not login_name or not password:
            messagebox.showerror("Ошибка", "Пароли не совпадают или пустые поля")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        json_output = json.dumps({"data": {"login_name": login_name,
                                           "password": hashed_password,
                                           "name" : name,
                                           "sex" : sex,
                                           "age" : age,
                                           "ves" : ves,
                                           "rost" : rost}, "action": "REGISTER"})

        client.send(json_output.encode())
        response = client.recv(1024).decode()
        messagebox.showinfo("Ответ сервера", response)
        reg_window.destroy()

    tk.Button(reg_window, text="Зарегистрироваться", command=send_register).pack()