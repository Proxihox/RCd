import pickle
from cryptography.fernet import Fernet

class user:
    def __init__(self, _uname, _passwd):
        self.uname: str = _uname
        self.passwd: str = _passwd
        self.active:bool = False
        #print(self.desc())
        pass
    def desc(self):
        return self.__class__.__name__ + " " + self.uname + " " + self.passwd


class Player(user):
    def __init__(self, _uname, _passwd):
        super().__init__(_uname, _passwd)

class Admin(user):
    def __init__(self, _uname, _passwd):
        super().__init__(_uname, _passwd)

def key_generation():
    key=Fernet.generate_key()
    with open('mykey.key','wb') as mykey:
        mykey.write(key)

#If users.pkl already exists and is not encrypted already this encrypts it
def encrypt_data(): 
    with open('mykey.key','rb') as file:
        key=file.read()
    cipher=Fernet(key)
    with open('users.pkl','rb')as file:
        data=file.read()
    try:
        cipher.decrypt(data)
    except:
        encrypted_data=cipher.encrypt(data)
        with open('users.pkl','wb') as file:
            file.write(encrypted_data)

def dump_data(users: dict[str,user]):
    with open('mykey.key','rb') as file:
        key=file.read()
    cipher=Fernet(key)
    pickled_data=pickle.dumps(users)
    encrypted_data=cipher.encrypt(pickled_data)
    with open('users.pkl','wb') as file:
        file.write(encrypted_data)

def load_users():
    with open('mykey.key','rb') as file:
        key=file.read()
    cipher=Fernet(key)
    with open('users.pkl','rb') as file:
        encrypted_data=file.read()
    decrypted_data=cipher.decrypt(encrypted_data)
    users=pickle.loads(decrypted_data)
    return users

def authenticate(users: dict[str, user], uname: str, passwd: str) -> bool:
    if uname in users:
        if users[uname].passwd == passwd and not users[uname].active:
            return True
    return False

def get_passwd(users: dict[str, user],uname:str):
    print(users[uname].passwd)
    return users[uname].passwd

def add_user(users: dict[str, user], _user: user):
    users[_user.uname] = _user
    dump_data(users)

def make_admin(users: dict[str, user], uname: str):
    users[uname].__class__ = Admin
    dump_data(users)

def init_admin():
    key_generation()
    users = {}
    users['admin'] = Admin('admin', 'admin')
    dump_data(users)