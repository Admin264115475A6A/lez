# Python 3.9.13

# modals that come with python v3.9
import random
import hashlib


# random number generator
#seedlocktest = int(3301)
#random.seed(seedlocktest)
x = []  # list
# seed genarator loop creates six numbers
for ii in range(6):
    A = random.randint(11, 99)
    x.append(A)

a = x[0]
b = x[1]
c = x[2]
d = x[3]
e = x[4]
f = x[5]

# my table for
ranZero = (a, b, c, d, e, f)
ranOne = a + b + c + d + e + f
ranTwo = a + 1 + b + 2 + c + 3 + d + 4 + e + 5 + f + 6
ranThree = a + 1 + 3 + b + 2 + 5 + c + 3 + 7 + d + 4 + 11 + e + 5 + 13 + f + 6 + 17


# seedOne is 16 in length
seedOne = ranOne * 16 * 2 ** 256
# seedTwo is 32 in length
seedTwo = ranTwo * 32 * 2 ** 256
# seedThr is 64 in length
seedThr = ranThree * 64 * 2 ** 256

# length of between 1000 1500
seed_gen = str(ranOne + seedOne + ranTwo + seedTwo + ranThree + seedThr * 16 ** 256)
seed_gen_int = int(ranOne + seedOne + ranTwo + seedTwo + ranThree + seedThr * 16 ** 256)


#sha512 hash for seed_gen
#witch is exported to blockchain

origin_seed = hashlib.sha512()
origin_seed.update(str(seed_gen).encode('utf-8'))
origin_seed.hexdigest()
hsh = origin_seed.hexdigest()

#writes to a seedgenTX.txt
f = open("C:/Users/vlad/OneDrive/Desktop/os/mint_tea/medusacoin/lenz-main/seedgenTX.txt", 'w')
#f.writelines()
f.writelines("seed_gen : ")
f.writelines(seed_gen)
f.writelines("\n")
f.writelines("origin_seed : ")
f.writelines(origin_seed.hexdigest())


f.close()
"""
print("****"*40)
#print("seedlocktest:",seedlocktest)
print("ranZero:",ranZero)
print("randOne:",ranOne)
print("ranTwo:",ranTwo)
print("ranThree:",ranThree)
print("****"*40)
print("seedOne:",seedOne)
print("seedTwo:",seedTwo)
print("seedThr:",seedThr)

print("****"*40)
print("seed_gerated:", seed_gen)
print("origin key",origin_seed.hexdigest())
"""
print("done... please check the seedgenTX.txt")
