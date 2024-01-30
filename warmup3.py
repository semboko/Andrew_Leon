def is_prime(n):
    # If n is prime, this function returns True
    # If n is not prime, this function returns False
    for i in range(2, n):
        # z is a remainder after the division of n by i
        z = n % i
        if z == 0:
            return False
    return True
        
counter = 0

for i in range(100, 100001):
    if is_prime(i):
        print(i)
        counter = counter + 1
        
print("The total amount of primes is ", counter)