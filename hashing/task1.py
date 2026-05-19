from Crypto.Hash import SHA256
import random
import string
import time

## a
def hashinput(text, size = 24):
    text_bytes = str(text).encode()
    hash = SHA256.new(text_bytes)
    truncated = bin(int(hash.hexdigest(), 16))[:size+2] ##convert to binary so we can truncate by 2 bit increments
    return hex(int(truncated,2))[2:]    ## convert back to hex for readability, and remove 0x

def generate_random_string():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


##b
plaintext = []
plaintext.append("t")
plaintext.append("u")
plaintext.append("hello")
plaintext.append("helln")
plaintext.append("this is a test")
plaintext.append("this is a uest")
plaintext.append("this is some more text. i am padding this out to test longer strings. i want to make sure it takes arbitrary inputs")
plaintext.append("uhis is some more text. i am padding this out to test longer strings. i want to make sure it takes arbitrary inputs")


hashedtext = []
for i in plaintext:
    hashedtext.append(hashinput(i))

for i in hashedtext:
    print(i)

## c
print("\n\n==============task 1c:===============\n\n")

def findcollisions(size):
    inputcount = 0
    hashdict = {}
    start = time.perf_counter()
    while True:
        plaintext = generate_random_string()
        hashedtext = hashinput(plaintext, size)

        if hashedtext in hashdict:
            end = time.perf_counter()
            break
        else:
            inputcount+=1
            hashdict[hashedtext] = plaintext

    print(plaintext, "has hash", hashedtext)
    print(hashdict[hashedtext], "has hash", hashedtext)
    print(f"number of inputs until found: {inputcount:,}")
    print(f"time until found: {end-start:.6f} seconds")


for i in range(8,52,2):
    print(f"bits: {i} \tpossible hashes: {pow(2,i):,}")
    findcollisions(i)
    print("\n")
