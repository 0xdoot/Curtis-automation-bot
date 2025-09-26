import os
import json
from web3 import Web3
from dotenv import load_dotenv
import time

# Load .env
load_dotenv()
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

# Setting RPC
RPC_URL = 'https://curtis.rpc.caldera.xyz/http'
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Ganti alamat kontrak dan load ABI
ARBITRUM_TO_CURTIS_ADDRESS = '0x990A3402F3358A1Ac9886c42d12A5C47aD97cb94' 
CURTIS_TO_ARBITRUM_ADDRESS = '0x0000000000000000000000000000000000000064'  

with open('abiBridgeArbitrumToCurtis.json', 'r') as f:
    ABI_ARBITRUM_TO_CURTIS = json.load(f)
with open('abiBridgeCurtisToArbitrum.json', 'r') as f:
    ABI_CURTIS_TO_ARBITRUM = json.load(f)

contractArbitrumToCurtis = web3.eth.contract(address=ARBITRUM_TO_CURTIS_ADDRESS, abi=ABI_ARBITRUM_TO_CURTIS)
contractCurtisToArbitrum = web3.eth.contract(address=CURTIS_TO_ARBITRUM_ADDRESS, abi=ABI_CURTIS_TO_ARBITRUM)

account = web3.eth.account.from_key(PRIVATE_KEY)
ADDRESS_WALLET = account.address

def send_bridge(contract, function_name, value_eth, jumlah, **kwargs):
    for i in range(jumlah):
        nonce = web3.eth.get_transaction_count(ADDRESS_WALLET)
        value_wei = web3.to_wei(value_eth, 'ether')
        func = getattr(contract.functions, function_name)
        # Argument dan value harus sesuai ABI kontrak!
        if function_name == 'withdrawEth':
            tx = func(ADDRESS_WALLET).build_transaction({
                'from': ADDRESS_WALLET,
                'nonce': nonce,
                'value': value_wei,
                'gas': 300000, # sesuaikan gas limit!
                'gasPrice': web3.to_wei('0.1', 'gwei')
            })
        elif function_name == 'sendTxToL1':
            tx = func(ADDRESS_WALLET, b'').build_transaction({
                'from': ADDRESS_WALLET,
                'nonce': nonce,
                'value': value_wei,
                'gas': 300000, # sesuaikan gas limit!
                'gasPrice': web3.to_wei('0.1', 'gwei')
            })
        else:
            raise Exception("Fungsi tidak didukung!")

        signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
        print(f"TX ke-{i+1} ({function_name}): {tx_hash.hex()}")
        # Tunggu konfirmasi
        result = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"TX confirmed! Block: {result['blockNumber']}")
        time.sleep(6)  # Optional: jeda supaya nonce benar.

# Eksekusi
print("Bridge Arb Sepolia ke Curtis 10x @ 0.2 ETH")
send_bridge(contractArbitrumToCurtis, "withdrawEth", 0.2, 10)
print("Bridge Curtis ke Arbitrum Sepolia 10x @ 0.1 ETH")
send_bridge(contractCurtisToArbitrum, "sendTxToL1", 0.1, 10)
print("SELESAI semua bridge!")
