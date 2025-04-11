import tkinter as tk
from tkinter import messagebox
import json

from utilities.center_windows import center_window


def AddFood(root, client, login_name):
    add_food_window = tk.Toplevel(root)
    add_food_window.title("Добавление")
    center_window(add_food_window, 300, 250)
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