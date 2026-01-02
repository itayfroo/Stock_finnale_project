import numpy as np
import random

def randomPrime():
    p = random.randint(2**63 ,2**64)
    a = random.randint(2,p-2)
    while (a**(p-1)%p !=1):
        p = random.randint(2 ** 63, 2 ** 64)
        print(p)
    return p

print(randomPrime())