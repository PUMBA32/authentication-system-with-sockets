import socket 
import os

from typing import List


class Client:
    def __init__(self, host: str = socket.gethostname(), port: int = 12344) -> None:
        self._port: int = port
        self._host: str = host

        menu = 
    
    
    def run(self) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self._host, self._port))  # Подключение клиента к серверу по его адресу
            while 1:
                req: str = self.get_request()
                resp: str = self.
        finally:
            client.close()  # Закрытие клиентского сокета  

    
    def get_user_input() -> List[str]:
          

    
if __name__ == '__main__':
    client: Client = Client()
    client.run()


