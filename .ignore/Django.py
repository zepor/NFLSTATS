import string
import random

def generate_secret_key():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(50))

print(generate_secret_key())
