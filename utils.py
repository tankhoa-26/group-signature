import math
import random

def square_and_multiply(x, n, p = None):
    '''
    Hàm cài đặt thuật toán bình phương và nhân tính nhanh lũy thừa x^n mod p với x, n, p là các số nguyên lớn (1024 bit)
    Input: Cơ số x nguyên, lũy thừa n nguyên, số nguyên tố p (option) (tất cả các số đều là số 1024 bit)
    Output: Kết quả của x^n hoặc x^n mod p
    '''

    # Chuyển số mũ n sang hệ nhị phân, dùng lstrip để cắt bỏ đi phần 0b trong chuỗi nhị phân sau khi chuyển đổi
    exp = bin(n).lstrip('0b')
    
    # Gán giá trị kết quả ban đầu là 1
    value = 1

    # Thuật toán square and multiply
    for i in exp:
        value = value ** 2
        
        # Nếu bit i là 1, biến kết quả được đem nhân cho cơ số x
        if i == '1':
            value = value * x

        # Biến kết quả mod cho p
        if p:
            value = value % p

    return value

def miller_rabin_primality_test(p):
    '''
    Hàm kiểm tra Miller-Rabin cho số nguyên p
    Input: Số nguyên p
    Output: Kết quả kiểm tra Miller-Rabin
    '''

    # Nếu p = 2, hiển nhiên p là số nguyên tố, trả về True
    if p == 2:
        return True

    # Nếu p chia hết cho 2, hiển nhiên p là hợp số, trả về False
    if (p % 2) == 0:
        return False

    # Do p là số nguyên tố nên p - 1 sẽ có dạng 2^s * m, do đó p1 = 2^s * m
    p1 = p - 1 
    # Khởi tạo ban đầu, s = 0, m = p1
    s = 0
    m = p1 
    
    # Đưa p1 về dạng 2^s * m với s > 0, m < p1, m lẻ
    while (m % 2) == 0:
        m = m >> 1
        s = s + 1

    # Đến đây, p1 = p - 1 = 2^s * m
    assert p - 1 == (2 ** s) * m

    num_of_miller_rabin_tests = 5

    # Kiểm tra Miller-Rabin
    for _ in range(num_of_miller_rabin_tests):
        # Chọn ngẫu nhiên số tự nhiên a từ 2 đến p - 1
        a = random.randrange(2, p - 1)

        # Đặt b = a^m (mod p)
        b = square_and_multiply(a, m, p)

        # Nếu b = 1 (mod p) thì trả về True
        if b == 1:
            return True

        # Cho chạy từ 0 đến s
        for _ in range(s):
            # Nếu b = 1 (mod p) thì trả về True
            if b == -1:
                return True

            # Gán b = b^2 (mod p)
            b = square_and_multiply(b, 2, p)

        # Trả về False
        return False 

    # Trả về True
    return True

def generate_big_primes(n, k = 1):
    '''
    Hàm khởi tạo số nguyên tố lớn (1024 bit)
    Input: n là số bit, k là số nguyên tố tạo ra (k mặc định bằng 1, tức là tạo ra 1 số nguyên tố 1024 bit)
    Output: 1 danh sách chứa k số nguyên tố được tạo ra (k >= 1)
    '''
    # Ở đây, ta cần đảm bảo rằng k > 0, số bit nằm trong khoảng từ 0 đến 4096 bit  
    assert k > 0
    assert n > 0 and n < 4096

    # Tạo một danh sách các số nguyên tố sẽ chứa các số nguyên tố tạo được sau này
    primes = []

    # Kiểm tra tính nguyên tố của x bằng kiểm tra Miller-Rabin
    while k > 0:
        x = random.getrandbits(n)

        if miller_rabin_primality_test(x):
            primes.append(x)
            k = k - 1

    # Trả về danh sách số nguyên tố 
    return primes

def extended_euclidean_algorithm(a, b):
    '''
    Hàm cài đặt thuật toán Euclid mở rộng
    Input: 2 số nguyên a, b
    Output: gcd là ước chung lớn nhất của a và b; x, y là 2 số nguyên sao cho ax + by = gcd
    '''

    # Nếu a = 0, dễ thấy ước chung lớn nhất của a và b là b và x, y là 0 và 1
    if a == 0:
        return b, 0, 1

    # Khi a != 0, gọi hàm đệ quy với 2 biến b mod a và a cho đến khi có 1 trong 2 số bằng 0
    gcd, x, y = extended_euclidean_algorithm(b % a, a)

    # Tìm x và y dựa vào kết quả của hàm đệ quy theo công thức:
    # x = y - (b // a) * x
    # y = x
    return gcd, y - (b // a) * x, x