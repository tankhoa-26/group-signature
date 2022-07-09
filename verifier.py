import nacl.encoding
import nacl.hash
from cryptomath.Algorithms.Algorithms import ModularInv, FastPower

HASHER = nacl.hash.sha256
class Verifier:
    def __init__(self):
        pass
    
    def verify(self, c, s1, s2, s3, s4, T1, T2, T3, m, a, a0, g, h, y, n, lambda_1, gamma_1):
        two_pow_lambda1 = pow(2, lambda_1)
        two_pow_gamma1 = pow(2, gamma_1)

        c = c % n
        temp1 = ( (FastPower(a0, c, n) * FastPower(T1, s1 - c * two_pow_gamma1, n) % n) * ModularInv((FastPower(a, s2 - c * two_pow_lambda1, n)*FastPower(y, s3, n)) % n, n) ) % n

        temp2 = FastPower(T2, s1 - c * two_pow_gamma1, n) * ModularInv( FastPower(g, s3, n), n ) % n

        temp3 = FastPower(T2, c, n) * FastPower(g, s4, n) % n

        temp4 = FastPower(T3, c, n) * FastPower(g, s1 - c * two_pow_gamma1, n) * FastPower(h, s4, n) % n 

        msg_ = str(g) + str(h) + str(y) + str(a0) + str(a) + str(T1) + str(T2) + str(T3) + str(temp1) + str(temp2) + str(temp3) + str(temp4) + m
        new_c_byte = HASHER(str.encode(msg_), encoder=nacl.encoding.HexEncoder)
        new_c = int.from_bytes(new_c_byte, "big") % n
        return (c == new_c)
