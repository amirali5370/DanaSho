import random
from models.user import User
def invite_generator():
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        code = ''.join(random.choice(string) for x in range(6))
        x = User.query.filter(User.invite_code==code).first()
        if x == None:
            break
    return code


def inviteAuth_generator():
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        code = ''.join(random.choice(string) for x in range(36))
        x = User.query.filter(User.invite_auth==code).first()
        if x == None:
            break
    return code

def authCode_generator():
    string = "123456789"
    while True:
        code = ''.join(random.choice(string) for x in range(6))
        if len(str(code)) == 6:
            x = User.query.filter(User.msg_code==code).first()
            if x == None:
                break
    return code