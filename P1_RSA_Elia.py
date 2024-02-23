# Algorithms Project 1 - RSA
# Objective: implement RSA Encryption and apply it to digital signature
import pandas as pd
import sys
import random
import math
import csv
import hashlib

def multiply(a, b):
    """
    Multiply two numbers using recursive multiplication algorithm.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of a and b.
    """

    if (a==0 or b==0):
        return 0
    elif (b==1):
        return a
    elif (a==1):
        return b
    elif (b%2==0): # if b is even
        return 2 * multiply(a, b//2)
    elif (b%2!=0): # if b is odd
        return a + (2 * multiply(a, b//2)) # b//2 is the floor division of b by 2
    else:
        return a * b

def FermatPrimalityTest(p):
    """
    Performs the Fermat primality test on a given number p.

    Args:
        p (int): The number to be tested for primality.

    Returns:
        bool: True if p is likely to be prime, False otherwise.
    """

    # 1 and negatives are not prime
    if p <= 1 :
        return False

    # if it's even then it's not prime
    if (p % 2 == 0):
        return False

    a = 2
    # first fermet's pass
    # if (a^n-1) % n != 1 then return False
    if (pow(a, p-1, p) != 1):
        return False
    a = 7
    # second fermet's pass
    # if (a^n-1) % n != 1 then return False
    if (pow(a, p-1, p) != 1):
        return False
    return True

def getPrime(minBits=256):
    """
    Generates a prime number with a minimum number of bits using the Fermat primality test.

    Args:
        minBits (int): The minimum number of bits for the generated prime number. Default is 256.

    Returns:
        int: A prime number with at least minBits number of bits.
    """

    num = 0
    while (not FermatPrimalityTest(num)):
        num = random.getrandbits(minBits)
        # sometimes getrandbits() returns a number with less bits than required
        # maybe because that most significant few bits are 0 and get trunkated
        if(num.bit_length() < minBits):
            num = multiply(num, 10000)
            num += 7919
        if(num.bit_length() < minBits):
            num = multiply(num, 10000)
            num += 3923
    return num

def isCoprime(a, b):
    """
    Check if two numbers are coprime.

    Args:
    a (int): First number.
    b (int): Second number.

    Returns:
    bool: True if the numbers are coprime, False otherwise.
    """
    return math.gcd(a, b) == 1

# returns the multiplicative inverse of a mod m
def getMultiplicativeInverse(a, m):
    """
    Returns the multiplicative inverse of a mod m.

    Args:
    a (int): The number for which the multiplicative inverse is to be found.
    m (int): The modulus.

    Returns:
    int: The multiplicative inverse of a mod m.
    """
    return pow(a, -1, m)

def RSA_key_generation():
    """
    Generates RSA keys and saves them to CSV files.

    Returns:
    None
    """
    p = getPrime()
    q = getPrime()
    n = multiply(p,q)

    phi = multiply(p-1, q-1)
    e = getPrime(128)
    while (not isCoprime(e, phi)):
        e = getPrime(128)

    d = getMultiplicativeInverse(e, phi)
    # to be completed
    pq = pd.Series([p,q])
    en = pd.Series([e,n]) # e and n are public keys
    dn = pd.Series([d,n]) # d and n are private keys
    pq.to_csv("p_q.csv", index=False, header=False)
    en.to_csv("e_n.csv", index=False, header=False)
    dn.to_csv("d_n.csv", index=False, header=False)
    print("done with key generation!")


def Signing(doc, key):
    """
    Signs a document using the RSA algorithm and saves the signature to a file.

    Args:
    doc (str): The name of the document to be signed.
    key (tuple): The RSA key (d, n).

    Returns:
    None
    """
    # open doc and read it
    with open(doc, mode ='r')as file:
        docData = file.read()

    # hash the document data and convert it to an integer
    message = int(hashlib.sha256(docData.encode()).hexdigest(), 16)

    # sign the message
    signature = pow(message, key[0], key[1])
    with open(doc+".signed", 'w') as f:
        f.write(docData + "\n")
        f.write(str(signature))
    print("\nSigned ...")


def verification(doc, key):
    """
    Verifies the signature of a document using the RSA algorithm.

    Args:
    doc (str): The name of the document to be verified.
    key (tuple): The RSA key (e, n).

    Returns:
    None
    """
    # open doc and read it
    with open(doc, mode ='r')as file:
        docLines = file.readlines()

    # the document data is all the lines except the last one
    docData = ''.join(docLines[:-1])
    # remove new line at the end of the document data which shouldn't be there
    if docData.endswith('\n'):
        docData = docData[:-1]

    # hash the document data and convert it to an integer
    message = int(hashlib.sha256(docData.encode()).hexdigest(), 16)

    # the signature is the last line
    signature = int(docLines[-1])

    # verify
    # decryptedSignature = pow(signature, e) mod n
    decryptedSignature = pow(signature, key[0], key[1])
    match = message == decryptedSignature
    # to be completed
    if match:
        print("\nAuthentic!")
    else:
        print("\nModified!")

# No need to change the main function.
def main():

    # part I, command-line arguments will be: python yourProgram.py 1
    if int(sys.argv[1]) == 1:
        RSA_key_generation()

    # part II, command-line will be for example: python yourProgram.py 2 s file.txt
    #                                       or   python yourProgram.py 2 v file.txt.signed
    else:
        (task, fileName) = sys.argv[2:]
        if "s" in task:  # do signing
            doc = fileName
            # read d_n.csv file
            with open('d_n.csv', mode ='r') as file:
                csvFile = csv.reader(file)
                d = int(next(csvFile)[0])
                n = int(next(csvFile)[0])
            key = (d, n) # key[0] is d and key[1] is n
            Signing(doc, key)
        else:
            # do verification
            doc = fileName
            with open('e_n.csv', mode ='r') as file:
                csvFile = csv.reader(file)
                e = int(next(csvFile)[0])
                n = int(next(csvFile)[0])
            key = (e, n) # key[0] is e and key[1] is n
            verification(doc, key)

    print("done!")


if __name__ == '__main__':
    main()
