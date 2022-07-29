#!/usr/bin/ python3

from web3 import Web3
import json
from secrets import infuraUrl, pubKeys, pKeys, currentShContract
import time

#lambda functions for rounding
ro1, ro2, ro4, ro6, ro8 = lambda x : round(x, 1), lambda x : round(x, 2), lambda x : round(x, 4), lambda x : round(x, 6), lambda x : round(x, 8)
z18 = 1000000000000000000 # 18 zeros


web3 = Web3(Web3.HTTPProvider(infuraUrl))


global EIP20_ABI
EIP20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')









# import current shardHive contract and convert into checksum
shV0002contract = Web3.toChecksumAddress(currentShContract)


# import public keys and convert into checksum format
sh0Pub, sh1Pub, sh2Pub = Web3.toChecksumAddress(pubKeys['shardHive0']), Web3.toChecksumAddress(pubKeys['shardHive1']), Web3.toChecksumAddress(pubKeys['shardHive2'])


# import private keys as variables
sh0p, sh1p, sh2p = pKeys['shardHive0'], pKeys['shardHive1'], pKeys['shardHive2']
#sh0p, sh1p, sh2p = Web3.toChecksumAddress(pKeys['shardHive0']), Web3.toChecksumAddress(pKeys['shardHive1']), Web3.toChecksumAddress(pKeys['shardHive2'])



# check Ether Balance
def fetchETHBalance(walletAddress):
	balanceInWei = web3.eth.getBalance(walletAddress)
	balanceEth = float(Web3.fromWei(balanceInWei, 'ether'))
	addressBalance = {'address': walletAddress, 'bal': balanceEth}
	return addressBalance


# my preference is for the balance i
def fetchErc20Balance(walletAddress, contractAddress):

	nonce = web3.eth.getTransactionCount(walletAddress)	
	contractObject = web3.eth.contract(address=contractAddress, abi=EIP20_ABI)
	walletBalance = contractObject.caller.balanceOf(walletAddress)
	addressBalance = {'address': walletAddress, 'bal': walletBalance}
	return addressBalance




def fetchErc20TotalSupply(contractAddress):

	#nonce = web3.eth.getTransactionCount(walletAddress)	
	contractObject = web3.eth.contract(address=contractAddress, abi=EIP20_ABI)
	walletBalance = contractObject.caller.totalSupply()
	balDiv18 = ro8(walletBalance / 1000000000000000000) # 18 zeros
	return balDiv18



# send Ether
def sendEther(fromAddress, fromAddresspk, toAddress, etherAmount):
	walletBalances = {'from0': None, 'from1': None, 'to0': None, 'to1': None}
	fetchFrom, fetchTo = fetchETHBalance(fromAddress), fetchETHBalance(toAddress)

	walletBalances['from0'] = fetchFrom
	walletBalances['to0'] = fetchTo


	print("\nWallet balances before sending")
	print(fetchFrom)
	print(fetchTo)

	nonce = web3.eth.getTransactionCount(fromAddress)
	tx = {'nonce': nonce,
		  'to': toAddress,
		  'value': web3.toWei(etherAmount, 'ether'),
		  'gas': 21000,
		  'gasPrice': web3.toWei(40, 'gwei'),
		  }

	signedTx = web3.eth.account.signTransaction(tx, fromAddresspk)
	tx_hash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
	print('\nsent transaction: ' + str(tx))

	# wait 20 seconds and check wallet balances again
	time.sleep(20)

	fetchFrom, fetchTo = fetchETHBalance(fromAddress), fetchETHBalance(toAddress)

	walletBalances['from1'] = fetchFrom
	walletBalances['to1'] = fetchTo

	print("\nWallet balances after sending")
	print(fetchFrom)
	print(fetchTo)



	return walletBalances







# amount is in units of 1 (18 decimals)

def sendErc20Token(fromAddress, fromPkey, toAddress, contractAddress, amount):
	#get the nonce.  Prevents one from sending the transaction twice
	nonce = web3.eth.getTransactionCount(fromAddress)

	contractObject = web3.eth.contract(address=contractAddress, abi=EIP20_ABI)

	oneToken = 1000000000000000000 # 18 zeros

	# Build a transaction that invokes this contract's function, called transfer
	contractTxn = contractObject.functions.transfer(
		toAddress,
		oneToken*amount,
		).buildTransaction({
		'chainId': 3, # for mainnet Ethereum transactions change this to 1.
		'gas': 100000,
		'maxFeePerGas': web3.toWei('2', 'gwei'),
		'maxPriorityFeePerGas': web3.toWei('1', 'gwei'),
		'nonce': nonce,
	})

	try:
		# sign the transaction
		signed_tx = web3.eth.account.sign_transaction(contractTxn, private_key=fromPkey)
	except Exception as e:
		print('failed signing the transaction')
		print(e)

	try:
		# send the transaction
		tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
		# get transaction hash
		txHashHex = str(web3.toHex(tx_hash))

		contractTxn.update({'txHash': txHashHex})


	except Exception as e:
		print('failed sending the transaction')
		print(e)

	return contractTxn





# slice first and last 4 digits of public key
def getAddrDict(inputAddress):
	outputDict = {'first': inputAddress[:4], 'last': inputAddress[-4:]}
	return outputDict


def writeJson(jsonOutAddr, jsonData):
	try:
		with open(jsonOutAddr, 'w') as fp1: json.dump(jsonData, fp1)
		functionOutput = ("\nSuccess Creating JSON at: " + str(jsonOutAddr) + "\n")

	except Exception as e:
		functionOutput = "\nFailed to create JSON. Error msg:\n" + str(e)

	return functionOutput




def readJson(jsonInAddr):
	with open(jsonInAddr, 'r') as r:
		jsonOutputDict = json.load(r)
	return jsonOutputDict




