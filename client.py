# network connection
import socket
# performing various tasks
import threading
# create username
import mysql.connector

user = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5006))
# database
# con = mysql.connector.connect(
#     host="localhost",
#     username='root',
#     password='',
#     database="db"
# )
#
# cursor = con.cursor()
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
#     message varchar(1024) not null,
#     username varchar(50) not null
# );""")


def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg == 'START':
                client.send(user.encode())
            else:
                print(msg)
        except:
            print("Error")
            client.close()
            break


def write():
    while True:
        msg = f"{user} : {input('')}"
        client.send(msg.encode())
        sql_query = """INSERT INTO Users (message, username) VALUES (%s, %s)"""
        values = (msg, user)
        cursor = con.cursor()
        cursor.execute(sql_query, values)
        con.commit()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
