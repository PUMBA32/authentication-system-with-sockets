import socket
import sqlite3 as sq


class Server:
    def __init__(self, host: str = socket.gethostname(), port: int = 12345) -> None:
        self._host: str = host
        self._port: int = port

        self._PATH_TO_DB: str = "D:\\Coding\\PYTHON\\webdev\\projects\\auth\\base.db"

        try:
            with sq.connect(self._PATH_TO_DB) as self.con:
                self.cur = self.con.cursor()

                self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        password TEXT                 
                    )""")
            print("[+] created connection with db")
        except sq.Error as e:
            print(f"[error] connection with db: {e}")


    def run(self) -> None: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            server.bind((self._host, self._port))
            server.listen()
            print("[i] listening...")
            while True:
                conn, add = server.accept()
                print(f"\n[+] new client-socket: {add}")
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('[error] Client serving failed.\n', e)
                    conn.send("FAILED".encode())
        finally:
            server.close()
            self.con.close()

    
    def serve_client(self, conn: socket.socket) -> None:
        req: list[str] = self.parse_request(conn)
        resp: str = self.handle_request(req)

        print(f"[i] - req: {req}\n    - resp: {resp}")

        if resp == "END":
            conn.close()
            print("[-] connection closed\n")
            return
        
        self.send_response(conn, resp)
        print("[i] response successfully sent")
        

    def parse_request(self, conn: socket.socket) -> list[str]:
        try: 
            buff = conn.recv(1024)
            request: str = buff.decode()
            return request.split('\n')
        except Exception as e:
            raise Exception(f"Parsing request error: {e}")
            
    
    def handle_request(self, req: list[str]) -> str:
        req_title: str = req[0]

        match req_title:
            case "CHECK_NAME": return self.check_name(req[1])
            case "ADD_USER": return self.add_user(req[1], req[2])
            case "CHECK_ACCOUNT": return self.check_account(req[1], req[2])
            case "END": return "END" 
            case _: return "FAILED"


    def check_name(self, name: str) -> str: 
        try:
            self.cur.execute("SELECT * FROM users WHERE name = ?", (name,))
            result = self.cur.fetchone()

            return "SUCCESSFUL" if result else "NO_USER"
        except sq.Error as e:
            raise Exception(f"Database. Checking name error: {e}")


    def add_user(self, name, pas) -> str: 
        try:
            self.cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, pas))
            self.con.commit()

            return "SUCCESSFUL"
        except sq.Error as e:
            raise Exception(f"Database. adding user error: {e}")
    

    def check_account(self, name, pas) -> str: 
        try:
            self.cur.execute("SELECT * FROM users WHERE name = ?, password = ?", (name, pas))
            result = self.cur.fetchone()

            return "SUCCESSFUL" if result else "BAD_PASSWORD"
        except sq.Error as e:
            raise Exception(f"Database. Checking account error: {e}")

    
    def send_response(self, conn: socket.socket, resp: str):
        try:
            conn.send(resp.encode())
        except Exception as e:
            raise Exception(f"Sending response error: {e}")


if __name__ == '__main__':
    server: Server = Server()
    server.run()