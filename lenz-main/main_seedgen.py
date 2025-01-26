#########################################################
##  M     M EEEEEEE DDD   U     U  SSS    AA            #
##  MM   MM E       D  D  U     U S      A  A           #
##  M M M M EEEEEE  D   D U     U  SSS  AAAAAA          #
##  M  M  M E       D  D  U    UU     S A    A          #
##  M     M EEEEEEE DDD    UUUU U SSSS  A    a COIN     #
##                                                      #
##  BY GRp59.com & ROOM 109                              #
#########################################################
# DISCRIPTION IN THE MEDUSA_COIN.ME
from cryptography.fernet import Fernet
from filehash import filehash_t
'''
    Fernet key is how you a going to store you blockchain till alphazero is 
    compleit please read the MEDUSA_COIN.ME under "blockchain_storage" section

this file is running the filehash.py

seed_data = filehash

build gpg sig

'''
seed = str(filehash_t)


bytes_seed = bytes(seed, 'utf-8')

key = Fernet.generate_key()
f = Fernet(key)
token_seed_en = f.encrypt(bytes_seed)
print("Token: ", token_seed_en)
token_seed_de = f.decrypt(token_seed_en)







