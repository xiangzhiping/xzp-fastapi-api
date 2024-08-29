import math


def is_prime(num):
    """ 判断一个数是否是素数 """
    if num <= 1:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True


def count_primes_in_range(m, n):
    """ 计算区间 [m, n] 内的素数个数 """
    count = 0
    for num in range(max(2, m), n + 1):
        if is_prime(num):
            count += 1
    return count


m = 10
n = 50
print(count_primes_in_range(m, n))
