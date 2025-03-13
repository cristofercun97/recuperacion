from models.entities.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from MySQLdb._exceptions import IntegrityError 

class ModelUser():
    def __init__(self,id, fullname, email, password):
        self.id=id
        self.fullname=fullname
        self.email= email
        self.password= password
        
    @classmethod 
    def login(cls, mysql, user):
        try:
            cursor = mysql.connection.cursor()
            sql = 'SELECT id, fullname, email, password FROM users WHERE email=%s'
            cursor.execute(sql, (user.email,))
            row = cursor.fetchone()
            
            if row:
                id, fullname, email, password_hash = row
                if check_password_hash(password_hash, user.password):
                    return User(id, fullname, email, None)
            return None 
        except Exception as e:
            raise Exception(f'Al parecer hubo un error: {e}')
        finally:
            cursor.close()
        
    @classmethod 
    def get_by_id(cls, mysql, id):
        try:
            cursor = mysql.connection.cursor()
            sql = 'SELECT id, fullname, email, password FROM users WHERE id=%s'
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            
            if row:
                return User(row[0], row[1], row[2], None)
            return None 
        except Exception as e:
            raise Exception(f'Al parecer hubo un error: {e}')
        finally:
            cursor.close()
        
    @classmethod 
    def register(cls, mysql, user):
        try:
            cursor = mysql.connection.cursor()
            sql = 'INSERT INTO users(fullname, email, password) VALUES(%s, %s, %s)'
            valid_password = generate_password_hash(user.password)
            cursor.execute(sql, (user.fullname, user.email, valid_password))
            mysql.connection.commit()
            return user
        except IntegrityError:
            raise Exception("El correo ya está registrado")
        except Exception as e:
            raise Exception(f'Al parecer hubo un error: {e}')
        finally:
            cursor.close()

