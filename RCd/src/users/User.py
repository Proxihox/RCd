import pickle
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


def load_users():
    users = pickle.load(open("users.pkl", "rb"))
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
    pickle.dump(users, open("users.pkl", "wb"))

def make_admin(users: dict[str, user], uname: str):
    users[uname].__class__ = Admin
    pickle.dump(users, open("users.pkl", "wb"))

def init_admin():

    users = {}
    users['admin'] = Admin('admin', 'admin')
    pickle.dump(users, open("users.pkl", "wb"))