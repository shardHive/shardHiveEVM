
# import functions from shardHiveEVM library
from shardHiveEVM import sendEther, sendAltCoin

# the shardHiveEVM program imports an Infura API URL via infuraSecret.py
# add your Infura URL to that program before running this script


# sample python functions for easily transferring Ether and ERC-20 alt coins

sendEthTest = sendEther(fromPublicKey, fromPrivateKey, toPublicKey, amount)


sendAltCoin = sendAltCoin(fromPublicKey, fromPrivateKey, toPublicKey, altCoinAddress, amount)


