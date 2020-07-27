from algosdk.v2client import algod
from algosdk import kmd,mnemonic
from algosdk.wallet import Wallet
from algosdk.future import transaction

//Get your KMD token and KMD address from your local node
kmd_token = "c314a11ced768a7084b963c28d38363b1c7322e3940f878118825a6063008716"
kmd_address = "http://127.0.0.1:7833"
# Create a kmd client
kcl = kmd.KMDClient(kmd_token, kmd_address)

#Create an algod client using PureStake API
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = ""
headers = {
   "X-API-Key": "//Your API Key Here",
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)

# get suggested parameters
sp = algod_client.suggested_params()

#print(dir(wallet))

# create a wallet object
# parameters to the Wallet function: wallet_name, wallet_password, kmd_client
wallet = Wallet("//Your wallet name here", "//Your wallet password here", kcl)

# Create accounts using the wallet

address = wallet.generate_key()
print("New account:", address)

address2 = wallet.generate_key()
print("New account:", address2)
