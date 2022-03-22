from ast import Try
from encodings import utf_8
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
from ntpath import join
import sqlite3
import json

from rest_createbase import *

#Создаем бд
conn = sqlite3.connect("mydatabase.db")

# cursor позволяет нам взаимодействовать с базой данных
cursor = conn.cursor()
try:
    a = print_all(conn, cursor, 'users')
except:
    create_base(conn, cursor)
    print("Data Base Created!")

# Класс сервера
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # определяем метод `do_GET` - выводится на экран содержимое таблицы. Имя таблицы определается по uri
    # http://localhost:8001/users - выведется содержимое таблицы users 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        a = print_all(conn, cursor, self.path[1:])
        # print(a)
        str_resp = "<table border='1'>"
        for i in a:
            str_resp += "<tr>"
            for j in i:
                str_resp += "<td>" + str(j) + "</td>"
            str_resp += "</tr>"
        str_resp += "</table>"
                
        # resp = ''.join(str)
        bb = bytearray(str_resp, 'utf8')
        self.wfile.write(bb)

# определяем метод `do_POST` - вставка строки в таблицу
# Примеры JSON:
# 1:
# {
#     "table_name": "events",
#     "id" : 3,
#     "label_time" : "2022-01-31 12:40:11",
#     "user_id" : 1,
#     "action_tipe" : "Визит",
#     "v_actions" : 5
# }
# 2:
# {
#     "table_name": "tarifs" 
#     "id" : 3, 
#     "name" : "Твой первый!"  ,
#     "start_date" : "2022-01-01" ,
#     "end_date" : "2022-12-01" ,
#     "v_min" : 400  ,
#     "v_sms" : 100 ,
#     "v_traffic" : 344
# }
# 3:
# {
#     "table_name": "users" ,
#     "id" : 3,
#     "current_balance" : 200.5  ,
#     "add_date" : "2002-01-01",
#     "age"  : 34 ,
#     "city" : "Москва",
#     "action_time" : "2022-01-30 15:40:11",
#     "action_tarif" : 2
# }
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        response = BytesIO()

        dict_body = json.loads(body)
        # print(list(dict_body.values()))
        try:
            add_line(conn, cursor, dict_body['table_name'], list(dict_body.values())[1:])
            response.write(b'Table updated!')
        except:
            response.write(b'Try again')
        
        self.wfile.write(response.getvalue())


# Изменение значения в таблице по наименованию таблицы и id строки
# Пример JSON:
# {
#     "table_name": "users" ,
#     "id" : 7,
#     "current_balance" : 333 
# }
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        response = BytesIO()

        dict_body = json.loads(body)
        try:
            change_field(conn, cursor, dict_body.pop('table_name'), dict_body.pop('id'), dict_body)
            response.write(b'Table updated!')
        except:
            response.write(b'Try again')
        self.wfile.write(response.getvalue())
    
# Удаление строки таблицы по имени таблицы и id
# Пример JSON:
# {
#     "table_name": "users" ,
#     "id" : 7,
# }
    def do_DELETE(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        response = BytesIO()

        dict_body = json.loads(body)
        try:
            del_field(conn, cursor, dict_body.pop('table_name'), dict_body.pop('id'))
            response.write(b'Table updated!')
        except:
            response.write(b'Try again')
        self.wfile.write(response.getvalue())

# Задаем параметры сервера
httpd = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
httpd.serve_forever()
