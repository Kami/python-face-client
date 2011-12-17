import random
import string

def get_random_string(length):
    value = ''.join(random.choice(string.letters + string.digits) for i in
                    xrange(length))
    return value
