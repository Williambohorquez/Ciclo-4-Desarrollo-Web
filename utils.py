import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
user_reguex = "^[a-zA-Z0-9_.-]+$"
palabra_reguex = "^[A-Za-z0-9_.-].*"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'



def isUsernameValid(user):
    if re.search(user_reguex, user):
        return True
    else:
        return False


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False

def isEmailValid(email):
    is_valid = validate_email(email)

    return is_valid


def isValidPic(pic):

    image = cv2.imread(pic)
    try:
        dummy = image.shape # Con esta línea se hace la verificación de que la imagen es utilizable
        return True
    except:
         # Aquí se retorna False por la excepción debido a que la imagen no está disponible o está corrupta
        return False

import cv2