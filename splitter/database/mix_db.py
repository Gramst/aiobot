from random import choice
from string import ascii_uppercase, ascii_lowercase

def gen_random_nick() -> str:
    return ''.join(choice(ascii_uppercase) for i in range(1)) + ''.join(choice(ascii_lowercase) for i in range(5)),