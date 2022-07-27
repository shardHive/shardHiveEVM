
#!/usr/bin/python3

from shardHiveEVM import *
from secrets import pKeys, pubKeys, altCoinAddress
from datetime import datetime, timedelta, date
from time import strftime, sleep
import numpy as np


shV0002contract = altCoinAddress

#lambda functions for rounding
ro1, ro2, ro4, ro6, ro8 = lambda x : round(x, 1), lambda x : round(x, 2), lambda x : round(x, 4), lambda x : round(x, 6), lambda x : round(x, 8)



justTime, justDate = strftime("%X"), strftime("%x")
t6="""
0----------|----------
///////////|/////////
--  shEVM v0.0.2  --
///////////|////////
-----------|------x
\n
Started on: {} at: {}
\n\n""".format(justDate, justTime)
print(t6)


sh0Pub, sh1Pub, sh2Pub = Web3.toChecksumAddress(pubKeys['shardHive0']), Web3.toChecksumAddress(pubKeys['shardHive1']), Web3.toChecksumAddress(pubKeys['shardHive2'])


sh0Addr, sh1Addr, sh2Addr = getAddrDict(sh0Pub), getAddrDict(sh1Pub), getAddrDict(sh2Pub)



shV002totalSupply = fetchAltTotalSupply(shV0002contract)


sh0EthBal, sh1EthBal, sh2EthBal = fetchETHBalance(sh0Pub)['bal'], fetchETHBalance(sh1Pub)['bal'], fetchETHBalance(sh2Pub)['bal']


sh0AltBal, sh1AltBal, sh2AltBal = fetchAltBalance(sh0Pub, shV0002contract), fetchAltBalance(sh1Pub, shV0002contract), fetchAltBalance(sh2Pub, shV0002contract)





# wallet sums
sum01, sum02, sum12, sum012 = sh0AltBal + sh1AltBal, sh0AltBal + sh2AltBal, sh1AltBal + sh2AltBal, sh0AltBal + sh1AltBal + sh2AltBal
sumDict = {'s01': sum01, 's02': sum02, 's12': sum12, 's012': sum012}

print("Total Supply: " + str(shV002totalSupply))
print('\nWallet group ownership')
for sumKey in list(sumDict.keys()):
	currentOwnership = ro2(sumDict[sumKey] / shV002totalSupply * 100)
	print(str(sumKey) + '  ' + str(currentOwnership) + '%')


print('\nsh0 Address: ' + str(sh0Addr['last']) + '  ETH: ' + str(ro4(sh0EthBal)) + '  sHive: ' + str(ro2(sh0AltBal)))
print('sh1 Address: ' + str(sh1Addr['last']) + '  ETH: ' + str(ro4(sh1EthBal)) + '  sHive: ' + str(ro2(sh1AltBal)))
print('sh2 Address: ' + str(sh2Addr['last']) + '  ETH: ' + str(ro4(sh2EthBal)) + '  sHive: ' + str(ro2(sh2AltBal)))
print('\n')


try:
	s12a = sendAltCoin(sh0Pub, sh0p, sh2Pub, shV0002contract, 120000)
	print(s12a)
except Exception as e:
	print(e)

print("\nSleep 12 seconds in between transactions\n")
sleep(12)

try:
	s12b = sendAltCoin(sh1Pub, sh1p, sh2Pub, shV0002contract, 12000000)
	print(s12b)
except Exception as e:
	print(e)



sh0dict = {'walletAddress': sh0Pub, 'ethBal': sh0EthBal, 'altContract': shV0002contract, 'shBal': sh0AltBal}
sh1dict = {'walletAddress': sh1Pub, 'ethBal': sh1EthBal, 'altContract': shV0002contract, 'shBal': sh1AltBal}
sh2dict = {'walletAddress': sh2Pub, 'ethBal': sh2EthBal, 'altContract': shV0002contract, 'shBal': sh2AltBal}

shUsers = [sh0dict, sh1dict, sh2dict]




#for user in shUsers: print(user)


# send 1000 tokens between participants
#s01, s10, s12, s21, s02, s20 = None, None, None, None, None, None



justTime, justDate = strftime("%X"), strftime("%x")
print("\n\n----------------------------")
print("Finished shV002 DeFi Test on: " + str(justDate) + " at: " + str(justTime))
print("----------------------------\n")


