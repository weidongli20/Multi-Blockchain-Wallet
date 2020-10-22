import os
import subprocess
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

from bit import wif_to_key, PrivateKeyTestnet
from bit.network import NetworkAPI

from dotenv import load_dotenv

from constants import *

load_dotenv()
mnemonic = os.getenv('MNEMONIC')

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

def derive_wallets(mnemonic, coin, numdriv=3):
    command = (f'./derive -g --mnemonic="{mnemonic}" '
            f'--coin="{coin}" --numderive={numdriv} '
            '--cols=path,address,privkey,pubkey --format=json')

    p = subprocess.Popen(command, 
                         stdout=subprocess.PIPE, 
                         shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    #print(keys)
    return keys

def priv_key_to_account(coin, priv_key):
    if coin == BTC:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    elif coin == ETH:
        return Account.from_key(priv_key)
    else:
        print("Pleae check the coin")

def create_tx(coin, account, to, amount):
    if coin == ETH:
            gasEstimate = w3.eth.estimateGas(
                {"from": account.address, 
                 "to": to, 
                 "value": amount}
            )
            return {
                "from": account.address,
                "to": to,
                "value": amount,
                "gasPrice": w3.eth.gasPrice,
                "gas": gasEstimate,
                "nonce": w3.eth.getTransactionCount(
                    account.address),
            }

    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(
            account.address, 
            [(to, amount, BTC)])
    else:
        print("Pleae check the coin")

def send_tx(coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed = account.sign_transaction(tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(
            signed.rawTransaction)
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed)
    else:
        print("Please check the coin")

if __name__ == "__main__":
    test = input ("Rung a test? (y/n) :")
    if test.lower() == 'y':
        coins = {}
        coin = ETH  # coin = BTCTEST
        coins[coin] = derive_wallets(mnemonic, coin)
        priv_key = coins[coin][0]['privkey']
        account = priv_key_to_account(coin, priv_key)
        recipient = coins[coin][1]['address']
        amount = 1  # amount = 0.00001 # for BTCTEST
        tx_created = create_tx(coin, account, recipient, amount)
        print(send_tx(coin, account, recipient, amount))

