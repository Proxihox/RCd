import socket
import threading
import subprocess
import os
import time
import random
from RCd.mail.mailer import send_otp
import RCd.config as config
from RCd.src.users.User import add_user, authenticate, load_users, init_admin, Player

ADDR = (config.SERVER, config.PORT)
FORMAT = 'UTF-8'
HOST_ADDRESS = socket.gethostbyname(socket.gethostname())
MSG_LENGTH = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def log(logstr):
    if(config.LOGS):
        with open("./log/logs.txt", "a") as f:
            f.write(logstr)

def is_valid_uname(uname):
    checks = [len(uname) == 8,
               uname[0:2].isalpha(),
               uname[2:4].isdigit(),
               uname[4].isalpha(),
                uname[5:8].isdigit()]
    return all(checks)

def make_otp():
    return random.randint(1000,9999)

def verify_email(conn,uname):
    email = uname + "@smail.iitm.ac.in"
    otp = make_otp()
    send_otp(email,otp)
    conn.send(f"An OTP has been sent to {email}\n".encode(FORMAT))
    conn.send(f"Enter OTP: ".encode(FORMAT))
    user_otp = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
    if(otp == int(user_otp)):
        conn.send("Email verified!\n".encode(FORMAT))
        return True
    else:
        return False


def create_pw_for_user(conn,uname):
    conn.send("Enter password: ".encode(FORMAT))
    passwd = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
    conn.send("Confirm password: ".encode(FORMAT))
    cpasswd = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
    if(passwd != cpasswd):
        conn.send("Passwords do not match, try again!\n".encode(FORMAT))
        return  
    else:
        add_user(user_list, Player(uname, passwd))
        conn.send("User created!\n".encode(FORMAT))

def start_auth(conn):
    global user_list
    for i in range(3):
        conn.send("Enter roll number: ".encode(FORMAT))
        uname = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
        uname = uname.lower()
        if(not is_valid_uname(uname)):
            conn.send("Invalid roll number, try again!\n".encode(FORMAT))
            continue
        if(uname not in user_list):
            conn.send(f"User not found, create new account with username {uname}? [Y/n]:\n".encode(FORMAT))
            resp = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
            if(resp == "Y" or resp == ""):
                conn.send("Creating new user...\n".encode(FORMAT))
                if(not config.VERIFY_MAIL or verify_email(conn,uname)):
                    create_pw_for_user(conn,uname)
            else:
                conn.send("Try logging in again!\n".encode(FORMAT))
                pass
        else:
            conn.send("Enter password: ".encode(FORMAT))
            passwd = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
            if(authenticate(user_list, uname, passwd)):
                conn.send("Logging in...\n".encode(FORMAT))
                return [True,user_list[uname]]
            else:
                conn.send("Wrong password or username, try again!\n".encode(FORMAT))
    return [False, None]

def handle_admin(conn): # give a menu with various options
    options = ["1. Test RC", "2. Add user", "3. Add new problem", "4. Exit"]
    for option in options:
        conn.send((option + "\n").encode(FORMAT))
    conn.send("Enter choice : \n".encode(FORMAT))
    choice = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
    if(choice == "1"):
        handle_player(conn)
    elif(choice == "2"):
        conn.send("Enter username: ".encode(FORMAT))
        uname = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
        conn.send("Enter password: ".encode(FORMAT))
        passwd = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
        add_user(user_list, Player(uname, passwd))
        conn.send("User added!\n".encode(FORMAT))
    elif(choice == '3'):
        pass
    elif(choice == "4"):
        conn.send("Exiting...\n".encode(FORMAT))
        conn.close()
        return
    else:
        conn.send("Enter an integer for your choice\n".encode(FORMAT))

def handle_player(conn,user): # create a subprocess and link its input output with the players socket.
    rc = subprocess.Popen(
        ["./RC.out"],
        #["python3", "reverseCoding.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    connected = True
    try:
        conn.send("RC session started!\n".encode(FORMAT))
        while connected:
            resp = rc.stdout.readline().strip()
            conn.send((resp+"\n").encode(FORMAT))
            msg = conn.recv(MSG_LENGTH).decode(FORMAT).strip()
            log(f"Recv: {msg}\n")
            rc.stdin.write(msg + "\n")
            rc.stdin.flush()
            time.sleep(10e-6)
            resp = rc.stdout.readline().strip()
            log(f"-> {resp}\n")
            conn.send((resp+"\n").encode(FORMAT))
    except Exception as e:
        log(f"[ERROR] {str(e)}\n")
    finally:
        rc.terminate()  # Ensure subprocess is terminated
        user_list[user.uname].active = False # Set user as inactive
        conn.close()


def handle_client(conn, addr): 
    auth, user = start_auth(conn) # Authenticate user 
    if(not auth):
        conn.send("Authentication failed, closing connection...\n".encode(FORMAT))
        conn.close()
        return
    if(user.__class__.__name__ == "Admin"): # Handle admins
        log(f"[NEW CONNECTION] {addr} connected as Admin.\n")
        handle_admin(conn)
        log(f"[DISCONNECTED] {addr} (adming) disconnected.\n")
    
    elif(user.__class__.__name__ == "Player"): # Handle players
        log(f"[NEW CONNECTION] {addr} connected.\n")
        handle_player(conn,user)
        log(f"[DISCONNECTED] {addr} disconnected.\n")
        

    

def start():
    global user_list
    if(os.path.exists("users.pkl")):
        user_list = load_users() # Load all users from file
    else:
        init_admin()
        user_list = load_users()
    print("PID: ", os.getpid())
    print(f"Connection command :\nnc {HOST_ADDRESS} {config.PORT}")
    server.listen()
    try:
        while True: # Accept connections and start a new thread for each
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Server is shutting down...")
    finally:
        server.close()  # Ensure the socket is properly closed
        print("[CLEANUP] Server socket closed. Exiting.")
    server.close()

if __name__ == "__main__":
    print("Starting server...") 
    user_list = load_users()
    start()
