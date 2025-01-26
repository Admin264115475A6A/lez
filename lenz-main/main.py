# chain is your difficulty level
from chain import Chain
#from main_seedgen import token_seed_en
from seedgen import seed_gen, hsh

i = 0

chain = Chain(20)


while(True):

    ## data is your holds you token_seed_en is your recovery key for your seedgen also your mircleroot
    ## token_seed_en
    data = (i, seed_gen, hsh)

    ## adds data to a pool list in a chain modual to be mind
    chain.add_to_pool(str(data))

    ## the minning from the pool list
    chain.mine()

    ## the chain.mind get put on the chain
    if i % 13 == 0:
        print('block',chain.blocks[i])
    i += 1
    print("\n")
    print("mined:\t",chain.blocks[i])
