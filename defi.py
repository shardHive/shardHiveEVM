
#!/usr/bin/python3

from shardHiveEVM import *
from secrets import pKeys, pubKeys, altCoinAddress
from datetime import datetime, timedelta, date
from time import strftime
import numpy as np


shV0002contract = altCoinAddress



#lambda functions for rounding
ro1, ro2, ro4, ro6, ro8 = lambda x : round(x, 1), lambda x : round(x, 2), lambda x : round(x, 4), lambda x : round(x, 6), lambda x : round(x, 8)


time = datetime.now()
dtRn = str(strftime("%x") + " " + strftime("%X"))
justTime, justDate = strftime("%X"), strftime("%x")
print("\n----------------------------")
print("Started shV002 test on: " + str(justDate) + " at: " + str(justTime))
print("----------------------------\n\n")



sh0Pub, sh1Pub, sh2Pub = pubKeys['shardHive0'], pubKeys['shardHive1'], pubKeys['shardHive2']

sh0EthBal, sh1EthBal, sh2EthBal = fetchETHBalance(sh0Pub)['bal'], fetchETHBalance(sh1Pub)['bal'], fetchETHBalance(sh2Pub)['bal']

shV002totalSupply = fetchAltTotalSupply(shV0002contract)

sh0Addr, sh1Addr, sh2Addr = getAddrDict(sh0Pub), getAddrDict(sh1Pub), getAddrDict(sh2Pub)

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



sh0dict = {'walletAddress': sh0Pub, 'ethBal': sh0EthBal, 'altContract': shV0002contract, 'shBal': sh0AltBal}
sh1dict = {'walletAddress': sh1Pub, 'ethBal': sh1EthBal, 'altContract': shV0002contract, 'shBal': sh1AltBal}
sh2dict = {'walletAddress': sh2Pub, 'ethBal': sh2EthBal, 'altContract': shV0002contract, 'shBal': sh2AltBal}


# send 100 tokens from shardHive0 to shardHive1 and inverse

#s01 = sendAltCoin(pubKeys['shardHive1'], pKeys['shardHive1'], pubKeys['jTest'], shV0002contract, 1000000)
#s10 = sendAltCoin(pubKeys['shardHive1'], pKeys['shardHive1'], pubKeys['shardHive0'], shV0002contract, 100)

try:    print(s01)
except: pass

try:    print(s10)
except: pass

justTime, justDate = strftime("%X"), strftime("%x")

print("\n\n----------------------------")
print("Finished shV002 test on: " + str(justDate) + " at: " + str(justTime))
print("----------------------------\n")
