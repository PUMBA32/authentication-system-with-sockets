import socket
import os
import sys


class Auth: 
    def __init__(self, client: socket.socket) -> None: 
        self.client: socket.socket = client

    
    def _cls(self) -> None:
        os.system("cls" if sys.platform == 'win32' else "clear")


    def __get_data_from_user(self) -> tuple[str]: 
        self._cls()

        while 1:
            name: str = input("Enter name: ").strip()

            if name == None or len(name) == 0:
                self._cls()
                print("Empty input. Try again.\n")
                continue

            pas: str = input("Enter password: ").strip()

            if pas == None or len(pas) == 0:
                self._cls()
                print("Empty input. Try again.\n")
                continue

            if len(pas) < 8:
                self._cls()
                print("Password must be more longer. Try again.\n")
                continue

            return name, pas


    def __check_name(self, name: str) -> str: 
        try: 
            request: str = f"CHECK_NAME\n{name}"
            self.client.send(request.encode())
            resp = self.client.recv(1024)
            return resp.decode()
        except Exception as ex:
            print(F"[error] Auth.__check name(): {ex}")
            return "FAILED"


    def check_username(self) -> tuple[str]: 
        name, pas = self.__get_data_from_user()
        check_result: str = self.__check_name(name)

        return name, pas, check_result 
    

    def send_request(self, request: str, err: str) -> str:
        try: 
            self.client.send(request.encode())  # Отправка запроса на сервер
            resp = self.client.recv(1024)  # Получение ответа от сервера
            return resp.decode()  # Отправка ответа 
        except Exception as ex:
            print(F"[error] {err}: {ex}") 
            return "FAILED"
    

class Login(Auth): 
    def __init__(self, client: socket.socket) -> None:
        super().__init__(client)


    def login(self) -> None: 
        name, pas, check_name_result = super().check_username()

        if check_name_result == "NO_USER":  # Если пользователя с таким ником нету
            self._cls()
            print("There is no user with such name. Try another.\n")
            return
        elif check_name_result == 'FAILED':  # Если появилась ошибка на сервере
            self._cls()
            print("Server error.\n")
            return
        
        check_account_result: str = self.__check_account(name, pas)

        match check_account_result:
            case "FAILED": print("Server error.\n")  # Появилась ошибка на сервере
            case "BAD_PASSWORD": print("Wrong password. Try again.\n")  # Пароль введен неправильно
            case "SUCCESSFUL": print("Welcome back!\n")  # Вход выполнен успешно 
            case _: print("Undefined server response.\n")  # Неизвестный ответ от сервера

    
    def __check_account(self, name: str, pas: str) -> str: 
        request = f"CHECK_ACCOUNT\n{name}\n{pas}"  # формирование запроса
        err = "Login.__check_account()"
        
        return self.send_request(request, err)


class Registration(Auth): 
    def __init__(self, client: socket.socket) -> None: 
        super().__init__(client)

    
    def registration(self) -> None: 
        name, pas, check_name_result = super().check_username()

        if check_name_result == "SUCCESSFUL":  # Если есть пользователь с таким ником           self._cls()
            print("There is user with such name. Try another.\n")
            return
        elif check_name_result == 'FAILED':  # Если появилась ошибка на сервере
            self._cls()
            print("Server error.\n")
            return
        
        add_result: str = self.__add_user(name, pas)

        match add_result:
            case "FAILED": print("Server error.\n")  # Появилась ошибка на сервере
            case "SUCCESSFUL": print("Account was created!\n")  # Аккаунт успешно создан 
            case _: print("Undefined server response.\n")  # Неизвестный ответ от сервера

    
    def __add_user(self, name: str, pas: str) -> str:
        request = f"ADD_USER\n{name}\n{pas}"  # Формирование запроса
        err = "Login.__add_user()"
        print(request)
        return self.send_request(request, err)


class Client:
    def __init__(self, host: str = socket.gethostname(), port: int = 12345) -> None: 
        self._port: int = port
        self._host: str = host  

    
    def show_menu(self) -> None:
        os.system("cls" if sys.platform == 'win32' else "clear")
        
        print("[1] Login")
        print("[2] Registration")
        print("[...] exit")


    def run(self) -> None: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self._host, self._port))
            
            while 1:
                self.show_menu()
                ch: str = input(">>> ").strip()

                match ch:
                    case "1": 
                        Login.login(Login(client))
                        input("*enter any key*")
                    case "2": 
                        Registration.registration(Registration(client))
                        input("*enter any key*")
                    case _: 
                        client.send("END".encode())
                        break
        finally:
            client.close()


if __name__ == '__main__':
    client: Client = Client()
    client.run()


