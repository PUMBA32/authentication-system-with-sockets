import socket 


class Server:
    def __init__(self, host: str = socket.gethostname(), port: str = 12345) -> None: 
        self._port: int = port
        self._host: int = host


    def run(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            server.bind((self._host, self._port))
            server.listen()

            while 1:
                conn, _ = server.accept()

                try:
                    self.serve_client(conn)
                except Exception as e:
                    print(f"[!] Client serving failed: {e}")
        finally:
            server.close()    


    def serve_client(self, conn: socket) -> None: 
        try:
            req = self.parse_request()
            resp = self.handle_request(req)
            self.send_response(resp)
        except Exception as e:
            self.send_error(conn, e)
        else:
            conn.close()

    
    def parse_request(self) -> str: ...


    def handle_request(self, request: str) -> str: ...


    def send_response(self, response: str) -> None: ...

    
    def send_error(self, conn: socket, exception: Exception) -> None: ...


if __name__ == '__main__':
    server = Server()
    server.run()