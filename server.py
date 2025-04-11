
import socket
import pyodbc
import json
from datetime import datetime

server_base = r'localhost\SQLEXPRESS'
database = 'db_logins'

dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_base};DATABASE={database};Trusted_Connection=yes'

IP = '127.0.0.1'
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)
print("Сервер запущен, ожидание подключения...")

conn, addr = server.accept()
print(f"Подключение от: {addr}")


def HarrisonBenedickt(sex, age, ves, rost):
    if sex == "male":
        ansv = 88.36 + (13.4 * ves) + (4.8 * rost) - (5.7 * age)
        return round(ansv, 2)
    elif sex == "female":
        ansv = 447.6 + (9.2 * ves) + (3.1 * rost) - (4.3 * age)
        return round(ansv, 2)




while True:
    request = json.loads(conn.recv(1024).decode())
    now = str(datetime.now())
    action = request["action"]
    print(f"Принято: \n{request}")

    if action == "ADMIN":
        print("Просмотр:")
        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            cursor.execute("SELECT [ID],[Time_log],[login] FROM [Clients]")
            rows = cursor.fetchall()

            result_str = ""
            for row in rows:
                result_str += f"\nID:{row[0]} Был в сети: {row[1]} Логин: {row[2]}"

            print("rez:")
            print(result_str)
            conn.send(result_str.encode())
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())

    elif action == "ADDFOOD":
        print("добавим еду")
        login_name = request["data"]["login_name"]
        food_name = request["data"]["food_name"]
        calories_per_100g = request["data"]["calories_per_100g"]
        grams_eaten = request["data"]["grams_eaten"]
        total_calories = request["data"]["total_calories"]

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            insert_query = "INSERT INTO  [Foods] ([login], [Name_food], [calories_per_100g], [grams_eaten], [total_calories]) VALUES (?, ?, ?, ?, ?)"
            values = (login_name, food_name, calories_per_100g, grams_eaten, total_calories)
            cursor.execute(insert_query, values)
            cursor.commit()
            conn_db.commit()
            print("Записано")
            # result_str = "Данные успешно сохранены"
            # conn.send(result_str.encode())

            cursor.close()
            conn_db.close()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            result_str = (f"Ошибка подключения: {e}")
            conn.send(result_str.encode())


    elif action == "GOAL":
        login_name = request["data"]["login_name"]

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            insert_name = "SELECT [Goal] FROM [Clients] WHERE [login] = ?"
            cursor.execute(insert_name, (login_name,))
            goal_from_bd = cursor.fetchone()
            conn.send(str(goal_from_bd[0]).encode())

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())



    elif action == "ALLFOOD":
        login_name = request["data"]["login_name"]

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            insert_all_food = "SELECT [Name_food], [grams_eaten], [total_calories] FROM [Foods] WHERE [login] = ?"
            cursor.execute(insert_all_food, (login_name,))
            rows = cursor.fetchall()

            total_calories_today= 0

            if not rows:
                conn.send("Сегодня вы ещё ничего не ели.".encode())
            else:
                result_str = ""
                for row in rows:
                    result_str += f"\n{row[0]} — {row[1]} г, {row[2]} ккал"
                    total_calories_today += float(row[2])

                conn.send(f"{result_str} \n\nВ сумме вы съели {total_calories_today} ккал.".encode())

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())


    elif action == "DELETEFOOD":
        print("")
        login_name = request["data"]["login_name"]

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()



            insert_delete_food = "DELETE FROM [Foods] WHERE [login] = ?"
            cursor.execute(insert_delete_food, (login_name,))
            cursor.commit()
            #
            # conn.send(result_str.encode())

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())




    elif action == "LOGIN":
        print("Вход:")
        print("")
        login_name = request["data"]["login_name"]
        password = request["data"]["password"]
        # name = request["data"]["name"]

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()
            values = (login_name, password)

            insert_check = "SELECT [ID] FROM [Clients] WHERE [login] = ? AND [Password] = ?"
            cursor.execute(insert_check, values)
            print("zapisal")
            IsLoginAndPassword = cursor.fetchall()

            insert_name = "SELECT [Name] FROM [Clients] WHERE [login] = ?"
            cursor.execute(insert_name, (login_name,))
            name_from_bd = cursor.fetchone()
            name_str = name_from_bd[0]

            if IsLoginAndPassword:
                json_output_from_server = json.dumps({"name": name_str, "action": "IN"})
                conn.send(json_output_from_server.encode())

            else:
                json_output_from_server = json.dumps({"name": "Нет такого пользователя", "action": "NO"})
                conn.send(json_output_from_server.encode())



            insert_time = f"UPDATE [Clients] SET [Time_log] = ? WHERE [login] = ? AND [Password] = ?"
            cursor.execute(insert_time, (now, login_name, password))
            conn_db.commit()
            print("time")
            cursor.close()
            conn_db.close()

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            conn.send(f"Ошибка подключения: {e}".encode())

    elif action == "REGISTER":

        print("Регистрация:")
        login_name = request["data"]["login_name"]
        Password = request["data"]["password"]
        name = request["data"]["name"]
        sex = request["data"]["sex"]
        age = int(request["data"]["age"])
        ves = float(request["data"]["ves"])
        rost = float(request["data"]["rost"])

        goal_of_calories = HarrisonBenedickt(sex, age, ves, rost)

        try:
            conn_db = pyodbc.connect(dsn)
            cursor = conn_db.cursor()

            insert_query = "INSERT INTO  [Clients] ([Login], [Password], [Name], [Sex], [Age], [Ves], [Rost], [Goal]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            values = (login_name, Password, name, sex, age, ves, rost, goal_of_calories)
            cursor.execute(insert_query, values)
            cursor.commit()
            conn_db.commit()
            print("Записано")
            result_str = "Данные успешно сохранены"
            conn.send(result_str.encode())

            cursor.close()
            conn_db.close()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            if "23000" in str(e):
                conn.send("Этот логин уже существует".encode())
            else:
                result_str = (f"Ошибка подключения: {e}")
                conn.send(result_str.encode())

    elif action == "BYE":
        print("Закрытие..")
        conn.send("Всего доброго".encode())
        break


conn.close()
server.close()
