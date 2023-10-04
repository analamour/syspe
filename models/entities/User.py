from werkzeug.security import check_password_hash, generate_password_hash

class User():

    def __init__(self, id, username, password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password(self,hashed_password,password):
        return check_password_hash(hashed_password, password)

# print(generate_password_hash('AJK1404'))
# devuelve el hash del pass
# pbkdf2:sha256:260000$SUSnXhMPQdcMhu1R$c9694c91759bde032f649209af584123642244234798adf26fbbda2fa2d8a5f8
