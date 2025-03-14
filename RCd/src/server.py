import socket
import threading
import subprocess
import os
import time
import random
from RCd.src import users
from RCd.mail.mailer import send_otp,send_forgot_passwd_mail
import RCd.config as config
from RCd.src.users.User import get_passwd,add_user, authenticate, load_users, init_admin, Player
import re

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
    conn.send(f"An OTP has been sent to {email}\n")
    conn.send(f"Enter OTP: ")
    user_otp = conn.recv(MSG_LENGTH)
    if(otp == int(user_otp)):
        conn.send("Email verified!\n")
        return True
    else:
        return False

def pw_check(pw,username,pw_strength):
    if pw_strength==1:
        return True
    min_pw_len=8
    pw_length=len(pw)
    error_strength_2={
        "uppercase_error":re.search(r"[A-Z]",pw),
        "lowercase_error":re.search(r"[a-z]",pw),
    }
    if pw_strength==2:
        if min_pw_len>pw_length or not all(error_strength_2.values()):
            return False
    error_strength_3={
        **error_strength_2,
        "digit_error":re.search(r"[0-9]",pw),
        "special_symbols_error":re.search(r"[!@#$%^&*(),.?\":{}|<>]",pw)
    }
    if pw_strength==1:
        if min_pw_len>pw_length or not all(error_strength_3.values()):
            return False
        if pw==username:
            return False
    return True

def create_pw_for_user(conn,uname):
    conn.send("Enter password: ")
    passwd = conn.recv(MSG_LENGTH)
    pw_checks=pw_check(passwd,uname,config.PASSWORD_SECURTIY_LEVEL)
    if not pw_checks:
        conn.send("This password is not strong enough try using uppercase, digits and special symbols\n")
        return
    conn.send("Confirm password: ")
    cpasswd = conn.recv(MSG_LENGTH)
    if(passwd != cpasswd):
        conn.send("Passwords do not match, try again!\n")
        return  
    else:
        add_user(user_list, Player(uname, passwd))
        conn.send("User created!\n")

def start_auth(conn):
    global user_list
    for i in range(3):
        conn.send("Enter roll number: ")
        uname = conn.recv(MSG_LENGTH)
        uname = uname.lower()
        if(not is_valid_uname(uname)):
            conn.send("Invalid roll number, try again!\n")
            continue
        if(uname not in user_list):
            conn.send(f"User not found, create new account with username {uname}? [Y/n]:\n")
            resp = conn.recv(MSG_LENGTH)
            if(resp.lower() == "Y" or resp == ""):
                conn.send("Creating new user...\n")
                if(not config.VERIFY_MAIL or verify_email(conn,uname)):
                    create_pw_for_user(conn,uname)
            else:
                conn.send("Try logging in again!\n")
                pass
        else:
            conn.send("Enter password: ")
            passwd = conn.recv(MSG_LENGTH)
            if(authenticate(user_list, uname, passwd)):
                conn.send("Logging in...\n")
                return [True,user_list[uname]]
            else:
                conn.send("Wrong password or username\n")
                conn.send("Forgot Password? [Y/n]: \n")
                response=conn.recv(MSG_LENGTH)
                if response=="Y" or response=="":
                    passwd=get_passwd(user_list,uname)
                    send_forgot_passwd_mail(uname,passwd)
                    conn.send("Mail succesfully sent, check your password and try logging in again!\n")
                else:
                    conn.send("Try again!\n")
                conn.send("Wrong password or username, try again!\n")
    return [False, None]

def handle_admin(conn): # give a menu with various options
    options = ["1. Test RC", "2. Add user", "3. Add new problem", "4. Exit"]
    for option in options:
        conn.send((option + "\n"))
    conn.send("Enter choice : \n")
    choice = conn.recv(MSG_LENGTH)
    if(choice == "1"):
        handle_player(conn)
    elif(choice == "2"):
        conn.send("Enter username: ")
        uname = conn.recv(MSG_LENGTH)
        conn.send("Enter password: ")
        passwd = conn.recv(MSG_LENGTH)
        add_user(user_list, Player(uname, passwd))
        conn.send("User added!\n")
    elif(choice == '3'):
        pass
    elif(choice == "4"):
        conn.send("Exiting...\n")
        conn.close()
        return
    else:
        conn.send("Enter an integer for your choice\n")

def handle_player(conn,user): # create a subprocess and link its input output with the players socket.
    user.qlim += 10
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
        conn.send("RC session started!\n")

        while (connected):
            user.qlim -= 1
            resp = rc.stdout.readline()
            conn.send((resp+"\n"))
            msg = conn.recv(MSG_LENGTH)
            log(f"Recv: {msg}\n")
            rc.stdin.write(msg + "\n")
            rc.stdin.flush()
            time.sleep(10e-6)
            resp = rc.stdout.readline()
            log(f"-> {resp}\n")
            conn.send((resp+"\n"))
            if(user.qlim == 0):
                connected = False
    except Exception as e:
        log(f"[ERROR] {str(e)}\n")
    finally:
        rc.terminate()  # Ensure subprocess is terminated
        user_list[user.uname].active = False # Set user as inactive
        conn.close()


def handle_client(conn, addr): 
    auth, user = start_auth(conn) # Authenticate user 
    if(not auth):
        conn.send("Authentication failed, closing connection...\n")
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
        
class conn_handler:
    def __init__(self, conn):
        self.conn = conn
    def send(self, msg):
        msg = msg.strip()+"\n"
        self.conn.send(msg.encode(FORMAT))
    def recv(self, length):
        s = ""
        while(s[-1:] != "\n"):
            ch = self.conn.recv(length).decode()
            if(ch != "\x08"):
                s += ch
            else:
                s = s[:-1]
            # print(repr(s),repr(s[-1]))
        return s.strip()
    def close(self):
        self.conn.close()
    

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
            conn_raw, addr = server.accept()
            conn = conn_handler(conn_raw)
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
    print("Success!")
