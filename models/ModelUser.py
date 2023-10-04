from.entities.User import User

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cur=db.connection.cursor()
            sql=f"""SELECT id, username, password, fullname FROM usuarios 
            WHERE username = {user.username}"""
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                user=User(row[0], row[1],User.check_password(row[2],user.password), row[3])
                return user
            else:
                None
        except Exception as ex:
            raise Exception(ex)
