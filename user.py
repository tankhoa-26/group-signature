import utils
import random
import nacl.encoding
import nacl.hash
import secrets
from cryptomath.Algorithms.Algorithms import ModularInv, FastPower

HASHER = nacl.hash.sha256
DEFAULT_BIT_LEN_RAND_ELEMENTS = 128

class User:
    
    def __init__(self):
        self.x_ex = 0
        self.x = 0
        self.A = 0
        self.e = 0

    #Join
    #Joint1 func
    def gen_random_element(self, n, g, h, lambda_2):
        two_pow_lambda_2 = FastPower(2, lambda_2)
        self.x_ex = secrets.randbelow(two_pow_lambda_2)
        r_ex = secrets.randbelow(n ** 2)
        
        C1 = ((FastPower(g, self.x_ex, n)) * (FastPower(h, r_ex, n))) % n
        return C1, r_ex

    def join3(self, a, n, alpha, beta, lambda_1, lambda_2):
        self.x = (FastPower(2, lambda_1, n) + (alpha * self.x_ex + beta % (FastPower(2, lambda_2)))) % n
        C2 = FastPower(a, self.x, n)
        return C2

    def join5(self, n, a, a0, A, e):
        print("A: ", A)
        print("e: ", e)
        print("a: ", a)
        print("a0: ", a0)
        print("x: ", self.x)
        print("n: ", n)

        
        print("left: ", FastPower(a, self.x, n) * a0 % n)
        print("right: ", FastPower(A, e, n))
        
        if ((FastPower(a, self.x, n) * a0 % n) == FastPower(A, e, n)):
            self.A = A
            self.e = e
            return True
        return False
    
    #Sign

    def sign(self, m, a, a0, g, h, y, l_p, n, lambda_1, lambda_2, gamma_1, gamma_2, epsilon, k):
        w = secrets.randbelow(2**(2 * l_p))
        T1 = self.A * FastPower(y, w, n)
        T2 = FastPower(g, w, n)
        T3 = FastPower(g, self.e, n) * FastPower(h, w, n) % n

        r1 = secrets.randbelow(2**(epsilon* (gamma_2 + k)) )
        r2 = secrets.randbelow(2**(epsilon* (lambda_2 + k)))
        r3 = secrets.randbelow(2**(epsilon* (gamma_1 + 2*l_p + k + 1)))
        r4 = secrets.randbelow(2**(epsilon* (2*l_p + k)))

        d1 = (FastPower(T1, r1, n) * ModularInv(FastPower(a, r2, n) * FastPower(y, r3, n), n)) % n
        d2 = FastPower(T2, r1, n) * ModularInv(FastPower(g, r3, n), n) % n
        d3 = FastPower(g, r4, n)
        d4 = (FastPower(g, r1, n) * FastPower(h, r4, n)) % n

        msg = str(g) + str(h) + str(y) + str(a0) + str(a) + str(T1) + str(T2) +str(T3) + str(d1) + str(d2) + str(d3) + str(d4) + str(m)

        #hash message
        c_byte = HASHER(str.encode(msg), encoder=nacl.encoding.HexEncoder)
        c = int.from_bytes(c_byte, "big") % n
        
        s1 = r1 - c * (self.e - pow(2, gamma_1)) 
        s2 = r2 - c * (self.x - pow(2, lambda_1))
        s3 = r3 - c * self.e * w    
        s4 = r4 - c * w            

        return (c, s1, s2, s3, s4, T1, T2, T3)



