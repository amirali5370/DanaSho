import random
import jdatetime
from models.interaction import Interaction
def likes_calculator(user):
    number = 0
    activisms = user.interactions.filter(Interaction.type=="activism", Interaction.status=="confirmed").all()
    for i in activisms:
        number += len(i.likes.all())
    return number

def is_liked(user, activism):
    user_like = user.likes.all()
    activism_like = activism.likes.all()

    return any(item in user_like for item in activism_like)

def comments_calculator(activism):

    return len(Interaction.query.filter(Interaction.type=="replay", Interaction.status=="confirmed",  Interaction.replay==activism.id).all())

def get_time():
    return jdatetime.datetime.today().strftime("%Y/%m/%d %H:%M")

def randomizer(op1, op2, op3, op4):
    shuffled_list = [op1, op2, op3, op4]
    random.shuffle(shuffled_list)
    return shuffled_list

def excerpt(input_list, number):
    return random.sample(input_list, number)
