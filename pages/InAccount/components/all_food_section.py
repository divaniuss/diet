import tkinter as tk
import json

from utilities.center_windows import center_window


def AllFood(root, client, login_name):
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

    json_output_all = json.dumps({"data": {"login_name": login_name}, "action": "ALLFOOD"})
    client.send(json_output_all.encode())
    response = client.recv(4096).decode()
    label_response.config(text=f"Вы сегодня съели:\n{response}")

    def Delete_Food():
        json_output = json.dumps({"data": {"login_name": login_name}, "action": "DELETEFOOD"})
        client.send(json_output.encode())
        label_response.config(text=f"Cегодня вы ничего не съели.")

    def Exit_from_all_food():
        all_food_window.destroy()

    tk.Button(all_food_window, text="Очистить", command=Delete_Food).pack(pady=(15, 10))
    tk.Button(all_food_window, text="Выйти", command=Exit_from_all_food).pack(pady=(15, 10))