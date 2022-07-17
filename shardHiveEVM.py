

from web3 import Web3
import json
from infuraSecret import secretInfuraUrl



web3 = Web3(Web3.HTTPProvider(secretInfuraUrl))



# check Ether Balance
def fetchETHBalance(walletAddress):
	balanceInWei = web3.eth.getBalance(walletAddress)
	balanceEth = float(Web3.fromWei(balanceInWei, 'ether'))
	addressBalance = {'address': walletAddress, 'balanceEth': balanceEth}
	return addressBalance



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







# sending an altCoin from one wallet to another. amount is in units of 1 (18 decimals)

def sendAltCoin(fromAddress, fromPkey, toAddress, contractAddress, amount):
	#get the nonce.  Prevents one from sending the transaction twice
	nonce = web3.eth.getTransactionCount(fromAddress)

	EIP20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501

	contractObject = web3.eth.contract(address=contractAddress, abi=EIP20_ABI)

	oneToken = 1000000000000000000

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
		print('success signing the transaction')
	except Exception as e:
		print('failed signing the transaction')
		print(e)

	try:
		# send the transaction
		tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
		# get transaction hash
		print('success sending the transaction')
		print('Transaction Hash: ' + str(web3.toHex(tx_hash)))

	except Exception as e:
		print('failed sending the transaction')
		print(e)

	return contractTxn


