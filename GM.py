import secrets
import json
from cryptomath.Primality.Primality import IsSophieGermainPrime
from cryptomath.Algorithms.Algorithms import ModularInv, ExtendedEuclidean, FastPower
from libnum.libnum.sqrtmod import jacobi


class GroupManager:
    
    def __init__(self):
        self.n = 0
        self.certificate = []
        self.__p1 = 0
        self.__q1 = 0
        self.__x = 0
        self.phi_n = 0

#======================Setup====================
    def genSysParam(self):
        print("Generate system parameter....")
        epsilon = 1
        k = 256
        l_p = 512 #l_p is size of the modulus to use
        lambda_2 = 1030
        lambda_1 = epsilon * (lambda_2 + k) + 2 + 10
        gamma_2 = lambda_1 + 2 + 10
        gamma_1 = epsilon * (gamma_2 + k) + 2 + 10
        return (lambda_1, lambda_2, gamma_1, gamma_2, epsilon, k, l_p)

    def getSophieGermainPrime(self):
        with open('SophieGermain.json', 'r') as f:
            data = json.load(f)
        index1 = secrets.randbelow(8)
        index2 = secrets.randbelow(8)
        while (index1 == index2):  index2 = secrets.randbelow(8)
        return (int( data[str(index1)]), int( data[str(index2)]))

    def setup(self, l_p = 1024):
        '''
        Pha SETUP, tạo các tham số hệ thống và khóa
        '''
        
        is_prime = False
        two_pow_l_p = pow(2, l_p)

        '''
            Unlock code phía dưới để tìm số nguyên tố Sophie Germain
            Từ đó tính được Safe Prime
            Tuy nhiên việc tính toán số Sophie Germain mất nhiều thời gian nên để tiện cho việc test
            ta gán cứng p1, q1 đã tìm được trước đó.
        '''
        #Tìm P1 là số nguyên tố Sophie Germain
        #p1 = secrets.randbelow(two_pow_l_p)
        # while (not IsSophieGermainPrime(p1)):
        #     p1 = secrets.randbelow(two_pow_l_p)
        #     print("p1: ",p1)

        #Tìm P2 là số nguyên tố Sophie Germain
        #q1 = secrets.randbelow(two_pow_l_p)
        # while (not IsSophieGermainPrime(q1)):
        #     q1 = secrets.randbelow(two_pow_l_p)
        #     print("q1: ", q1)
        print("Setup....")
        p1, q1 = self.getSophieGermainPrime()
        p = p1 * 2 + 1
        q = q1 * 2 + 1

        self.__p1 = p1
        self.__q1 = q1
        self.phi_n = p1 * q1

        n = p * q

        # Tạo a, a0, g, h thuộc QR(n) (bậc p'q') (default 14bits)
        elements = self.gen_random_element_of_cyclic_group(n)
        a = elements[0]
        a0 = elements[1] 
        g = elements[2]
        h = elements[3]
        
        #Tạo key pair 
        y = self.gen_random_secret_element(n, g)

        #Gom nhóm group public key 
        Y = (n, a, a0, y, g, h)
        print("Setup complete....")
        return (Y)


    def gen_random_element_of_cyclic_group(self, n):
        '''
        Hàm tạo k số có bậc p'q' thuộc cyclic group QR(n)
        '''
        #Tìm phần tử sinh
        gcd0 = gcd1 = gcd2 = 0

        while (gcd0 != 1 and gcd1 != 1 and gcd2 != 1):
            generator = secrets.randbelow(n)
            gcd0 = ExtendedEuclidean(generator, n)[0]    #check a nguyên tố cùng nhau với n -> a thuộc Zn*
            gcd1 = ExtendedEuclidean(generator - 1, n)[0]
            gcd2 = ExtendedEuclidean(generator + 1, n)[0]

        #Random 4 số mũ để tính 4 số a, a0, g, h

        ex1 = secrets.randbelow(self.phi_n)
        a = FastPower(generator, ex1, n)
        ex1 = secrets.randbelow(self.phi_n)
        a0 = FastPower(generator, ex1, n)
        ex1 = secrets.randbelow(self.phi_n)
        g = FastPower(generator, ex1, n)
        ex1 = secrets.randbelow(self.phi_n)
        h = FastPower(generator, ex1, n)

        return (a, a0, g, h)   

    #Tạo y = g^x (mod n)
    def gen_random_secret_element(self, n, g):
        self.__x = secrets.randbelow(self.phi_n)

        #y = g**x % n
        y = FastPower(g, self.__x, n)
        return (y)



    #==========================Join======================================
    def is_in_cyclic_group(self, element, n):
        #Use Jacobi
        return (jacobi(element, n) == 1)

    def join2(self, C1, n, lambda_2):
        two_pow_lambda2 = pow(2, lambda_2)

        if (self.is_in_cyclic_group(C1, n)):
            alpha = secrets.randbelow(two_pow_lambda2)
            beta = secrets.randbelow(two_pow_lambda2)
            return (alpha, beta)
        else: 
            return (False, False)

    def join4(self, C2, n, a0, gamma_1, gamma_2):
        if ( self.is_in_cyclic_group(C2, n)):
            two_pow_gamma1 = pow(2, gamma_1)
            two_pow_gamma2 = pow(2, gamma_2) 

            e = secrets.randbelow(2 * two_pow_gamma2) + two_pow_gamma1 - two_pow_gamma2
            e_inv = ModularInv(e, self.phi_n)
            A = FastPower((C2 * a0), e_inv, n) 

            self.certificate.append((e,A))

            return (e, A)
        return (False, False)



