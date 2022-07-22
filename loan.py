#!/usr/bin/python3

from shardHiveEVM import *
from datetime import datetime, timedelta, date
from time import strftime
import numpy as np


justTime, justDate = strftime("%X"), strftime("%x")
print("\n\n----------------------------")
print("Started shEVMv002 Lender Test on: "+str(justDate)+" at: "+str(justTime))
print("----------------------------\n")


# might need to add a variable that specifies if the loan is in ether or shEVM
# the helperNodeAddress variable is assigned to shardHiveEVMv002
# on main-net, restrict certain network activities to node operators

def hiveApplyForLoan(recipAddress, principal, termInDays, interestTier, helperNodeAddress):

    '''
    interest rates are associated with an applicants interestTier
    in production there would need to be a system for verifying the interest tier of users based on their wallet addresss, they would not be submitting the interest tier directly
    '''

    interestTiers = {1: 0.05, 2: 0.1, 3: 0.2}

    iRateDecimal = interestTiers[interestTier]
    iRatePercent = iRateDecimal * 100


    recipEthBalance = fetchETHBalance(recipAddress)
    recipShBalance = fetchAltBalance(recipAddress, helperNodeAddress)

    print("Wallet: " + str(recipAddress[:4]) + " - " + str(recipAddress[-4:]))
    print("ETH Balance: " + str(ro4(recipEthBalance['bal'])))
    print("shEVM Balance: " + str(ro1(recipShBalance)))
    print("Requesting: " + str(principal) + " ETH")
    print("Repayment in: " + str(termInDays) + " days")
    print("Interest rate: " + str(iRatePercent) + "%")

    loanDict = {'recip': (str(recipAddress[:4]) + " - " + str(recipAddress[-4:])), 'principal': principal, 'term': termInDays}
    return loanDict

loanTest = hiveApplyForLoan(sh1Pub, 30, 1095, 2, currentShContract)

print('\nLoan function output:' + str(loanTest))

justTime, justDate = strftime("%X"), strftime("%x")
print("\n----------------------------")
print("Finished shEVMv002 Lender Test on: " + str(justDate) + " at: " + str(justTime))
print("----------------------------\n")
