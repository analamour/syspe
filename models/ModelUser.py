from.entities.User import User

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cur=db.connection.cursor()
            sql=f"""SELECT id, username, password, fullname FROM usuarios 
            WHERE username = '{user.username}'"""
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                user=User(row[0], row[1],User.check_password(row[2],user.password), row[3])
                return user
            else:
                None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            cur=db.connection.cursor()
            sql=f"""SELECT id, username, fullname FROM usuarios 
            WHERE id = '{id}'"""
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                logged_user=User(row[0], row[1],None, row[2])
                return logged_user
            else:
                None
        except Exception as ex:
            raise Exception(ex)
