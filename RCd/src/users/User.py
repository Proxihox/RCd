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

def load_key():
    with open('mykey.key','rb') as mykey:
        key=mykey.read()
        return key

def encrypt_data(decrypted):
    f=Fernet(load_key())
    encrypted=f.encrypt(decrypted)
    return encrypted

def decrypt_data(encrypted):
    f=Fernet(load_key())
    with open('users.pkl','rb') as users:
        decrypted=f.decrypt(encrypted)
        return decrypted

def load_users():
    users = decrypt_data(pickle.load(open("users.pkl", "rb")))
    return users

def dump_data(users: dict[str,user]):
    encrypted=encrypt_data(users)
    pickle.dump(encrypted,open('users.pkl','wb'))

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

    users = {}
    users['admin'] = Admin('admin', 'admin')
    dump_data(users)