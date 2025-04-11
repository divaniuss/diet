import json
import hashlib
import tkinter as tk
from tkinter import messagebox

from utilities.center_windows import center_window


def register(root, client):
    reg_window = tk.Toplevel(root)
    reg_window.title("Регистрация")
    center_window(reg_window, 300, 400)

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
        name = name_entry.get().strip()
        sex = sex_entry.get().strip().lower()
        age = age_entry.get().strip()
        ves = ves_entry.get().strip()
        rost = rost_entry.get().strip()
        password = password_entry.get().strip()
        password_confirm = password_confirm_entry.get().strip()

        fields = [login_name, name, sex, age, ves, rost, password, password_confirm]
        if not all(fields):
            messagebox.showerror("Ошибка", "Убедитесь, что все поля заполнены.")
            return

        try:
            age = int(age)
            ves = float(ves)
            rost = float(rost)
        except ValueError:
            messagebox.showerror("Ошибка", "Убедитесь что рост, вес и возраст введены корректно.")
            return


        if sex != "male" and sex != "female":
            messagebox.showerror("Ошибка", "Ваш пол может быть Male или Female")
            return

        if password != password_confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
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