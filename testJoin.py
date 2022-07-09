import user
import GM
# n, a, alpha, beta, x_ex, lambda_1, lambda_2

def Join():
    C1, x_ex = user.gen_random_element()
    alpha, beta = GM.join2(C1)
    C2 = user.join3(alpha, beta, x_ex)
    ok = GM.join4(C2) 
    print("Join OK")
