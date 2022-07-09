import json
import secrets
from cryptomath.Primality.Primality import IsSophieGermainPrime

with open('SophieGermain.json', 'r') as f:
        data = json.load(f)
        for i in range (8):
            if (not IsSophieGermainPrime(int(data[str(i)]))): 
                print(int(data[str(i)]))