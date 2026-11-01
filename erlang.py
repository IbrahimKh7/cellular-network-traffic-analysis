import math

def blocking_B(N:int, A:float):
    # Check correct values of traffic and channels
    if N < 0 :
       raise ValueError("Number of channels(N) must be non negative")
    if A < 0 :
        raise ValueError("Traffic(A) must be non negative")    
    if N == 0 :
        return 1.00   
    if A == 0 :
        return 0.00    
        
    e=1.00 #First element of the denominator
    sum_denominator= e #denominator 
    for i in range(1, N+1):
        e=e*(A/i)
        sum_denominator= sum_denominator+e
    return e/sum_denominator
    # B = 1.0
    #for i in range(1, N + 1):
    ## B = A * B / (i + A * B) Claude Ai version

def channels_N(A:float, B:float):
    if B<=0 or B>=1:
        raise ValueError("Blockign must be between 0 and 1 (0,1)")
    N=1 
    G=blocking_B(N,A)
    while G > B:
        N+=1
        G=blocking_B(N,A)
    return N
    
def capacity_A(N: int, B: float):
    if N <= 0:
        raise ValueError("Number of channels must be positive")

    if B <= 0 or B >= 1:
        raise ValueError("Blocking must be between 0 and 1")

    A = N / 4
    G = blocking_B(N, A)

    # Initial guess G is too high
    while G > B:
        A -= A / 100
        G = blocking_B(N, A)
       

    # Initial guess G is below the target B 
    last_valid_A = A 

    while G <= B:
        last_valid_A = A # If A=1 and got G=0.009 then next iteration A=1.001 and G=0.011 the secodn A got use out of the loop bu the previous one is the currect toletable traffic
        A += A / 100
        G = blocking_B(N, A)

    return last_valid_A

if __name__ == "__main__":
    N = int(input("Enter N number of channels: "))
    A = float(input("Enter the Traffic: "))
    print(blocking_B(N, A))
    print("Your circuit can deal with up to", capacity_A(N, 0.01)) #0.01 or 0.001
    print("Your circuit should have", channels_N(A, 0.01), "number of channels")
