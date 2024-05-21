import streamlit as st
from Crypto.PublicKey import RSA #keep this library
import base64

#determine key size    
def keyPairGen(e, t):
    d = pow(e, -1, t)
    kPrivate = d
    
def isPrime(num):
    if(num > 1):
        for i in range(2, (num//2)+1):
         if((num % i) == 0):
            num = 0
            #not prime
         else:
            num = 1
            #is prime
        return num

def eCondition(e, t):
    while True:
        if(isPrime(e) == 1 and e >= t and t % e == 0):
            return e
        else:
            print("Please re-enter (e) as it is a prime number and satisfies conditions.")
            
    
print("Enter two different prime numbers, (P) and (Q):")
p = int(input())
q = int(input())
while True:
    if(p == q):
        print("Please enter different numbers:")
        p = int(input())
        q = int(input())
    else:
        break
    
n = p * q
t = (p - 1) * (q - 1)
print(f"Choose a number (E) that has the following conditions:\n1. Must be prime\n2. Must be less than {t}\n3. Must not be a factor of {t}")
e = eCondition(t)
    
kPrivate = keyPairGen(e, t)