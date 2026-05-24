import time
from bcrypt import *
import nltk
from multiprocessing import Pool, cpu_count
from nltk.corpus import words
from userInfo import *

nltk.download("words")

shadow_text = """Bilbo:$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq
Gandalf:$2b$08$J9FW66ZdPI2nrIMcOxFYI.q2PW6mqALUl2/uFvV9OFNPmHGNPa6YC
Thorin:$2b$08$J9FW66ZdPI2nrIMcOxFYI.6B7jUcPdnqJz4tIUwKBu8lNMs5NdT9q
Fili:$2b$09$M9xNRFBDn0pUkPKIVCSBzuwNDDNTMWlvn7lezPr8IwVUsJbys3YZm
Kili:$2b$09$M9xNRFBDn0pUkPKIVCSBzuPD2bsU1q8yZPlgSdQXIBILSMCbdE4Im
Balin:$2b$10$xGKjb94iwmlth954hEaw3O3YmtDO/mEFLIO0a0xLK1vL79LA73Gom
Dwalin:$2b$10$xGKjb94iwmlth954hEaw3OFxNMF64erUqDNj6TMMKVDcsETsKK5be
Oin:$2b$10$xGKjb94iwmlth954hEaw3OcXR2H2PRHCgo98mjS11UIrVZLKxyABK
Gloin:$2b$11$/8UByex2ktrWATZOBLZ0DuAXTQl4mWX1hfSjliCvFfGH7w1tX5/3q
Dori:$2b$11$/8UByex2ktrWATZOBLZ0Dub5AmZeqtn7kv/3NCWBrDaRCFahGYyiq
Nori:$2b$11$/8UByex2ktrWATZOBLZ0DuER3Ee1GdP6f30TVIXoEhvhQDwghaU12
Ori:$2b$12$rMeWZtAVcGHLEiDNeKCz8OiERmh0dh8AiNcf7ON3O3P0GWTABKh0O
Bifur:$2b$12$rMeWZtAVcGHLEiDNeKCz8OMoFL0k33O8Lcq33f6AznAZ/cL1LAOyK
Bofur:$2b$12$rMeWZtAVcGHLEiDNeKCz8Ose2KNe821.l2h5eLffzWoP01DlQb72O
Durin:$2b$13$6ypcazOOkUT/a7EwMuIjH.qbdqmHPDAC9B5c37RT9gEw18BX6FOay
"""

## turn user into strings
def str_convert(text):
    lines = text.splitlines()
    return lines

## goal split slat from hash
def extract_hash(text):
    newuser = UserInfo(
        text.split(':')[0],
        text.split('$')[1],
        text.split('$')[2],
        text.split('$')[3][:22],
        text.split('$')[3][22:],
        text
    )
    return newuser


def check_chunk(args):
    chunk, stored_hash = args

    for word in chunk:
        if checkpw(word.encode(), stored_hash):
            return word

    return None



def main():
    print("user indexes 0-14")
    myindex = input("input indexes to work on, comma separated (1,2,3): ")

    lst = str_convert(shadow_text)

   #contain extracted user data for decryption
    userList = []
    for i in lst:
        userList.append(extract_hash(i))

    ## list of all possible passwords
    word_list = [
        i for i in words.words() 
        if 6 <= len(i) <= 10
    ]

    ## user password unfo converted to bytes for checking
    string_list = myindex.split(",")

    if myindex.strip().lower() == "all":
        myuserList = userList
    else:
        int_list = [int(i) for i in string_list]
        myuserList = [userList[i] for i in int_list]

    print(myuserList)
    print("checking words:")
    for username in myuserList:
        start = time.perf_counter()
        print("finding password for", username.user)
        userbytes = username.userStr.split(":")[1].encode()

        cores = cpu_count()
        chunk_size = max(1, len(word_list) // cores)

        chunks = [
            word_list[i: i + chunk_size]
            for i in range(0, len(word_list), chunk_size)
        ]

        with Pool(cores) as pool:
            results = pool.map(
                check_chunk,
                [(chunk, userbytes) for chunk in chunks]
            )

        password = None

        for r in results:
            if r is not None:
                password = r
                break
            
        if password is not None:

            end = time.perf_counter()
            total = end - start
            print("found password: ")
            print(password)
            username.password = password
            with open("passwords-time.txt", "a+") as file:
                file.write(f"{username.user} : {username.password} : time {total}\n")

        else:
            print("password not found")

if __name__ == '__main__':
    main()