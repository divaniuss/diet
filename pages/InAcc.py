import json
import socket
import tkinter as tk
from tkinter import messagebox

from pages.center_windows import center_window


def InAccount(name, root, login_name, client):
    login_in_window = tk.Toplevel(root)
    login_in_window.title(f"Добро пожаловать {name}")
    center_window(login_in_window, 350, 300)

    def AddFood():
        add_food_window = tk.Toplevel(root)
        add_food_window.title("Добавление")
        center_window(add_food_window, 300, 180)
        add_food_window.configure(bg="#f0f0f0")

        tk.Label(add_food_window, text="Добавьте то, что вы только что съели:").pack(pady=(10, 5))

        tk.Label(add_food_window, text="Название:").pack()
        add_food_entry = tk.Entry(add_food_window)
        add_food_entry.pack(pady=5)

        tk.Label(add_food_window, text="Калории на 100 г:").pack()
        add_cal_entry = tk.Entry(add_food_window)
        add_cal_entry.pack(pady=5)

        tk.Label(add_food_window, text="Съедено грамм:").pack()
        add_weight_entry = tk.Entry(add_food_window)
        add_weight_entry.pack(pady=5)

        def Send_new_food():
            food_name = add_food_entry.get()

            try:
                calories_per_100g = float(add_cal_entry.get())
                grams_eaten = float(add_weight_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Калории и граммы должны быть числами")
                return

            total_calories = round((calories_per_100g / 100) * grams_eaten, 2)

            json_output = json.dumps({
                "data": {
                    "login_name": login_name,
                    "food_name": food_name,
                    "calories_per_100g": calories_per_100g,
                    "grams_eaten": grams_eaten,
                    "total_calories": total_calories
                },
                "action": "ADDFOOD"
            })

            client.send(json_output.encode())
            add_food_window.destroy()

        tk.Button(add_food_window, text="Сохранить", font=("Segoe UI", 11), width=25, command=Send_new_food).pack(
            pady=(15, 10))

    def AllFood():
        all_food_window = tk.Toplevel(root)
        all_food_window.title("Ваш рацион сегодня:")
        center_window(all_food_window, 300, 280)
        all_food_window.configure(bg="#f0f0f0")

        tk.Label(all_food_window, text="Ваш рацион сегодня:").pack(pady=(10, 5))

        label_response = tk.Label(all_food_window, text="", width=0, height=0, borderwidth=1, relief="solid")
        label_response.pack(pady=(10, 5))

        goal_label_response = tk.Label(all_food_window, text="", width=0, height=0)
        goal_label_response.pack(pady=(10, 5))

        json_output_goal = json.dumps({"data": {"login_name": login_name}, "action": "GOAL"})
        client.send(json_output_goal.encode())
        response_goal = client.recv(4096).decode()
        goal_label_response.config(text=f"Ваша цель:{response_goal} ккал")

        json_output = json.dumps({"data": {"login_name": login_name}, "action": "ALLFOOD"})
        client.send(json_output.encode())
        response = client.recv(4096).decode()
        label_response.config(text=f"Вы сегодня съели:\n{response}")


        def Delete_Food():
            json_output = json.dumps({"data": {"login_name": login_name}, "action": "DELETEFOOD"})
            client.send(json_output.encode())
            # response = client.recv(4096).decode()
            label_response.config(text=f"Cегодня вы ничего не съели.")

        def Exit_from_all_food():
            all_food_window.destroy()

        tk.Button(all_food_window, text="Очистить", command=Delete_Food).pack(pady=(15, 10))
        tk.Button(all_food_window, text="Выйти", command=Exit_from_all_food).pack(pady=(15, 10))


    def Exit():
        login_in_window.destroy()

    button_width = 30
    button_pad_y = 10
    tk.Button(login_in_window, text="Добавить новую еду", width=button_width, command=AddFood).pack(pady=button_pad_y)
    tk.Button(login_in_window, text="Посмотреть, что вы сегодня съели", width=button_width, command=AllFood).pack(pady=button_pad_y)
    tk.Button(login_in_window, text="Выйти",width=button_width, command=Exit).pack(pady=(button_pad_y, 20))