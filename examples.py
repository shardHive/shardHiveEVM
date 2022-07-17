
# Import (earlier version) of the shardHive EVM library
from shardHiveEVM import sendEther, sendAltCoin

# the shardHiveEVM program imports an Infura API URL via secretInfura.py
# add your Infura URL to that program before running this script


# sample python functions for easily transferring Ether and ERC-20 alt coins

sendEthTest = sendEther(fromPublicKey, fromPrivateKey, toPublicKey, amount)

sendAltCoin = sendAltCoin(fromPublicKey, fromPrivateKey, toPublicKey, altCoinAddress, amount)
