import random

def DNA(length):
    return ''.join(random.choice('CGTA') for _ in range(length))

