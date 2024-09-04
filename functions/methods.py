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