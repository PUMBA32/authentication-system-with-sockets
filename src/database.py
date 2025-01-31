import sqlite3

from typing import Any, List


class Database:
    def __init__(self, path_to_db: str = "D:\\Coding\\PYTHON\\webdev\\projects\\auth") -> None: 
        self.__PATH_TO_DB: str = path_to_db


    def search_user(self, name: str) -> bool: 
        users_names: List[str] = self.__get_users_names()
        for u_name in users_names:
            if name == u_name:
                return True
        return False 
    

    def is_there_account(self, name: str, pas: str) -> bool: 
        users_list: List[Any] = self.__get_users_list()

        for u_name, u_pas in users_list:
            if u_name == name and u_pas == pas:
                return True

            if u_name == name and u_pas != pas:
                return False
        
        return False


    def add_user(self, name: str, pas: str) -> None: ...

    def __get_users_names(self) -> List[str]: ...

    def __get_users_list(self) -> List[Any]: ...

