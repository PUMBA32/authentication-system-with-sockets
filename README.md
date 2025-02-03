# Client-Server console auth system in Python

For get more practice with sockets in python i decided to wrtie cli authentication system, using sockets and SQLite.
This program is divided into two parts: Client and Server. 

## How client works

1. <b>Initialization and connection.</b> The program begins to work with the creation of a socket and connect to the server on a given host and port.
   
2. <b>Menu</b>. After connecting, the client offers a menu with two main options: Login (Login) and Registration (Registration).
   
3. <b>Login and registration</b>. When choosing an input or “registration” option, the program requests a name and password with the user. These data are sent to the server to check or add a new user.

4. <b>Server answers</b>. The server processes requests and sends back the results (for example, successful registration, incorrect password, etc. The client application processes these answers and displays relevant messages to the user. 


## How server works
...
