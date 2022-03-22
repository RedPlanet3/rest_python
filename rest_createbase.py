from cmath import nanj
import sqlite3

# #Создаем бд
# conn = sqlite3.connect("mydatabase.db")

# # cursor позволяет нам взаимодействовать с базой данных
# cursor = conn.cursor()

def create_base(conn, cursor):
    # Создаем таблицу events
    cursor.execute("""CREATE TABLE events 
                    (id INTEGER auto_increment NOT NULL PRIMARY KEY,
                    label_time TEXT,
                    user_id INTEGER NOT NULL,
                    action_tipe TEXT,
                    v_actions INTEGER);""")

    # Сохраняем изменения
    conn.commit()

    # Создаем таблицу tarifs
    cursor.execute("""CREATE TABLE tarifs 
                    (id INTEGER auto_increment NOT NULL PRIMARY KEY,
                    name TEXT NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    v_min INTEGER NOT NULL,
                    v_sms INTEGER NOT NULL,
                    v_traffic INTEGER NOT NULL);""")

    conn.commit()

    # Создаем таблицу users
    cursor.execute("""CREATE TABLE users 
                    (id INTEGER auto_increment NOT NULL PRIMARY KEY,
                    current_balance REAL NOT NULL,
                    add_date TEXT,
                    age INTEGER NOT NULL,
                    city TEXT,
                    action_time TEXT,
                    action_tarif INTEGER NOT NULL);""")

    conn.commit()

    # Вставляем множество данных в таблицу используя безопасный метод "?"
    users = [(1, 0.0,"2002-01-01",40,"Москва","2022-01-30 15:40:11",1),
            (2, 199.0,"2018-05-15",25,"Москва","2022-03-05 00:30:56",2)]
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?)", users)
    conn.commit()

    # Вставляем множество данных в таблицу используя безопасный метод "?"
    tarifs = [(1, "БезПереплат","2020-01-01","2021-01-01",300,150,1024),
                (2, "Максимум","2021-11-15","2030-01-01",800,500,16384)]
    cursor.executemany("INSERT INTO tarifs VALUES (?,?,?,?,?,?,?)", tarifs)

    conn.commit()

    # Вставляем множество данных в таблицу используя безопасный метод "?"
    events = [(1, "2022-01-30 15:40:11",1,"Звонок",5),
                (2 ,"2022-01-30 15:40:11",1,"смс",1)]
    cursor.executemany("INSERT INTO events VALUES (?,?,?,?,?)", events)

    conn.commit()

# Вывод на экран
def print_all(conn, cursor, table):
    sql = "SELECT * FROM " + table
    cursor.execute(sql)
    return(cursor.fetchall()) # or use fetchone()

# Вставка
def add_line(conn, cursor, table_name, fields):
    sql = "INSERT INTO " + table_name + " VALUES (" + "?" + ",?"*(len(fields) - 1) + ");"
    cursor.execute(sql, fields)
    conn.commit()
# Изменения данных
def change_field(conn, cursor, table_name, id, fields):

    key = list(fields.keys())[0][:]
    val = str(fields[key])[:]
    sql = "UPDATE "+ table_name +" SET " + key + "=" + val+ " WHERE id=" + str(id) +";"
    cursor.execute(sql)
    conn.commit()

# Удаление строк
def del_field(conn, cursor, table_name, id):

    sql = "DELETE FROM "+ table_name +" WHERE id=" + str(id) +";"
    cursor.execute(sql)
    conn.commit()
