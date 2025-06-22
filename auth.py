# auth.py
from database import add_user, verify_user

def register(username, email, password):
    try:
        add_user(username, email, password)
        return True, "Registro exitoso"
    except:
        return False, "Error: Email ya registrado"

def login(email, password):
    if verify_user(email, password):
        return True, "Login exitoso"
    return False, "Error: Credenciales inválidas"