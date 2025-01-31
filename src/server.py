import socket 
import os
import sys

from database import Database
from typing import List


class Server:
    def __init__(self, host: str = socket.gethostname(), port: str = 12345) -> None: 
        self._port: int = port
        self._host: int = host
        
        self.db: Database = Database()

    
    def __cls(self) -> None:
        os.system("cls" if sys.platform == 'win32' else 'clear')


    def run(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            server.bind((self._host, self._port))  # Привязка сервера к определенному адресу
            server.listen()  # Прослушивание входящих подключений

            while 1:
                conn, _ = server.accept()  # Принятие подключений клиента 

                try:
                    self.serve_client(conn)  # Обработка сообщений от клиента
                except Exception as e:
                    self.__cls()
                    print(f"[!] Client serving failed: {e}")
        finally:
            server.close()  # Прекращение работы сервера (закрытие серверного сокета)


    def serve_client(self, conn: socket.socket) -> None: 
        try:
            req: List[str] = self.parse_request(conn)  # Разбиение запроса на список ключевых элементов
            resp = self.handle_request(req)  # Обработка запроса
            self.send_response(conn, resp)  # Отправка ответа от сервера
        except Exception as e:
            self.send_error(conn, e)  # Отправка ошибки в случае неполадок
        else:
            conn.close()  # Закрытие соединения с клиентом

    
    def parse_request(self, conn: socket.socket) -> List[str]: 
        data: str = conn.recv(1024).decode()  # Данные от клиента в объеме 1024 байт
        split_data: List[str] = data.split("\n")

        if len(split_data) != 3:
            raise Exception("[!!] Request content error")
        
        return split_data


    def handle_request(self, request: List[str]) -> str:
        req_type: str = request[0]  # Тип запроса
        name: str = request[1]  # Имя пользователя
        pas: str = request[2]  # Пароль от аккаунта пользователя

        if req_type == 'ADD':  # Добавление пользователя в базу 
            self.db.add_user(name, pas)
        elif req_type == 'IS_THERE':  # Проверка на наличия аккаунта в базе  
            return "DONE" if self.db.is_there_account(name, pas) else "FAILED"
        elif req_type == 'SEARCH_USER':  # Проверка на наличие пользователя в базе
            return "DONE" if self.db.search_user(name) else "FAILED"
        else:
            return "REQUEST TYPE FAILED"        

        
    def send_response(self, conn: socket.socket, response: str) -> None:
        try:
            conn.send(response.encode())  # Отправка ответа клиенту
        except Exception:
            raise Exception("[!!] Sending response failed")

    
    def send_error(self, conn: socket.socket, e: Exception) -> None:
        try:
            conn.send(e.encode())  # Отправка ошибки клиенту
        except Exception as e:
            raise Exception("[!!] Sending error failed")


if __name__ == '__main__':
    server = Server()
    server.run()