#!/usr/bin/python3

from shardHiveEVM import *
from secrets import pKeys, pubKeys
from datetime import datetime, timedelta, date
from time import strftime
import numpy as np

#lambda functions for rounding
ro2, ro4, ro6, ro8 = lambda x : round(x, 2), lambda x : round(x, 4), lambda x : round(x, 6), lambda x : round(x, 8)


time = datetime.now()
dtRn = str(strftime("%x") + " " + strftime("%X"))
justTime, justDate = strftime("%X"), strftime("%x")
print("\n----------------------------")
print("Started shV002 test on: " + str(justDate) + " at: " + str(justTime) + "\n")
print("\n----------------------------")



#print(pubKeys.keys())
sh0Pub, sh1Pub = pubKeys['shardHive0'], pubKeys['shardHive1']

#sh0Addr, sh1Addr = getAddrDict(sh0Pub), getAddrDict(sh1Pub)


#sh0Balance, sh1Balance = fetchETHBalance(sh0Pub), fetchETHBalance(sh1Pub)

#print('sh0 Address: ' + str(sh0Addr['last']) + '  ETH: ' + str(ro4(sh0Balance['bal'])))
#print('sh1 Address: ' + str(sh1Addr['last']) + '  ETH: ' + str(ro4(sh1Balance['bal'])))


#fromAddress, fromPkey, toAddress, contractAddress, amount):

# send 100 tokens from shardHive0 to shardHive1 and inverse

#s01 = sendAltCoin(pubKeys['shardHive0'], pKeys['shardHive0'], pubKeys['shardHive1'], shV0002contract, 100)

#s10 = sendAltCoin(pubKeys['shardHive1'], pKeys['shardHive1'], pubKeys['shardHive0'], shV0002contract, 100)



#print('\nOutput')
#print(send10)


# check Ether Balance
def fetchETHBalance(walletAddress):
	balanceInWei = web3.eth.getBalance(walletAddress)
	balanceEth = float(Web3.fromWei(balanceInWei, 'ether'))
	addressBalance = {'address': walletAddress, 'bal': balanceEth}
	return addressBalance



def fetchAltBalance(walletAddress, contractAddress):

	
	nonce = web3.eth.getTransactionCount(walletAddress)
	
	#print("\nNonce: " + str(nonce))

	EIP20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501

	contractObject = web3.eth.contract(address=contractAddress, abi=EIP20_ABI)

	walletBalance = contractObject.caller.balanceOf(walletAddress)

	#oneToken = 1000000000000000000 # 18 zeros
	balDiv18 = walletBalance / z18
	return balDiv18



sh0Addr, sh1Addr = getAddrDict(sh0Pub), getAddrDict(sh1Pub)

sh0AltBal, sh1AltBal = fetchAltBalance(sh0Pub, shV0002contract), fetchAltBalance(sh1Pub, shV0002contract)

sh0EthBal, sh1EthBal = fetchETHBalance(sh0Pub)['bal'], fetchETHBalance(sh1Pub)['bal']

print('sh0 Address: ' + str(sh0Addr['last']) + '  ETH: ' + str(ro4(sh0EthBal)) + '  sHive: ' + str(ro2(sh0AltBal)))
print('sh1 Address: ' + str(sh1Addr['last']) + '  ETH: ' + str(ro4(sh1EthBal)) + '  sHive: ' + str(ro2(sh1AltBal)))



"""
sh0Contract, sh1Contract = fetchAltBalance(sh0Pub, shV0002contract).caller, fetchAltBalance(sh0Pub, shV0002contract).caller

sh0Bal, sh1Bal = sh0Contract.balanceOf(sh0Pub), sh1Contract.balanceOf(sh1Pub)


print('\nOutput')
print(sh0Bal/z18)
print(sh1Bal/z18)

sm01 = ro6((sh0Bal + sh1Bal)/z18)
print(sm01)


# send 100 tokens from shardHive0 to shardHive1 and inverse

#s01 = sendAltCoin(pubKeys['shardHive0'], pKeys['shardHive0'], pubKeys['shardHive1'], shV0002contract, 1000000)

#s10 = sendAltCoin(pubKeys['shardHive1'], pKeys['shardHive1'], pubKeys['shardHive0'], shV0002contract, 100)

sh0Contract, sh1Contract = fetchAltBalance(sh0Pub, shV0002contract).caller, fetchAltBalance(sh0Pub, shV0002contract).caller

sh0Bal, sh1Bal = sh0Contract.balanceOf(sh0Pub), sh1Contract.balanceOf(sh1Pub)


print('\nOutput')
print(sh0Bal/z18)
print(sh1Bal/z18)

sm01 = ro6((sh0Bal + sh1Bal)/z18)
print(sm01)

"""

justTime, justDate = strftime("%X"), strftime("%x")

print("\n----------------------------")
print("\nFinished shV002 test on: " + str(justDate) + " at: " + str(justTime))
print("----------------------------\n")
