
from sklearn.cluster import k_means


class SystemParam:
    lambda_1 = 0
    lambda_2 = 0
    gamma_1 = 0
    gamma_2 = 0
    epsilon = 0
    k = 0
    l_p= 0

    def __init__(self, sysParam):
        self.lambda_1 = sysParam[0]
        self.lambda_2 = sysParam[0]
        self.gamma_1 = sysParam[2]
        self.gamma_2 = sysParam[3]
        self.epsilon = sysParam[4]
        self.k = sysParam[5]
        self.l_p = sysParam[6]

    def initialize(self, sysParam):
        pass



