from email import message
import random
import utils
from GM import GroupManager
from user import User
from verifier import Verifier
import testJoin

# DEFAULT_BIT_LEN_RAND_ELEMENTS = 1024
#pha setup
group_manager =  GroupManager()
Y = group_manager.setup(128)
epsilon, k, lambda_1, l_p, lambda_2, gamma_1, gamma_2 = group_manager.getSysParam()
n, a, a0, y, g, h = Y
#Tạo user1
user1 = User(epsilon, k, l_p, lambda_1, lambda_2, gamma_1, gamma_2, n, a, a0, y, g, h)
#Join
C1, x_ex, r_ex = user1.gen_random_element()
alpha, beta = group_manager.join2(C1)
C2 = user1.join3(alpha, beta, x_ex)
e, A = group_manager.join4(C2)
if (not user1.join5(A, e)): exit()
#Sign
secret_ = "helloman"
c, s1, s2, s3, s4, T1, T2, T3 = user1.sign(secret_)
print(c)
print(s1)
print(s2)
print(s3)
print(s4)
print(T1)
print(T2)
print(T3)
#Verify
verifier1 = Verifier(epsilon, k, l_p, lambda_1, lambda_2, gamma_1, gamma_2, n, a, a0, y, g, h)
verifier1.verify(c, s1, s2, s3, s4, T1, T2, T3, secret_)