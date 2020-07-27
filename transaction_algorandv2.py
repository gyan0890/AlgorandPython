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

accounts = wallet.list_keys()

# get wallet information
info = wallet.info()
print(info)
# print("Wallet name:", info["wallet"]["name"])

# # create a sender account
sender_address = accounts[0]
print("Sender account:", sender_address)

# # create a receiver account
receiver_address = accounts[1]
print("Sender account:", receiver_address)
send_amount = 100

# Create and sign transaction
txn = transaction.PaymentTxn(sender_address, sp, receiver_address, send_amount)

# # write transaction to file
#txns = [txn]
#transaction.write_to_file([txn], "pathtofile.tx")

## ------------------------------ ##
walletid = wallet.id


wallethandle = kcl.init_wallet_handle(walletid, "// Your wallet password")
accountkey = kcl.export_key(wallethandle, "// Your wallet password", accounts[0])
mn = mnemonic.from_private_key(accountkey)
print("Account Mnemonic: ", mn)

#### Backing up a wallet with mnemonic
# # get the wallet's master derivation key
# mdk = wallet.export_master_derivation_key()
# print("Master Derivation Key:", mdk)

# get the backup phrase
#backup = mnemonic.from_master_derivation_key(mdk)
#print("Wallet backup phrase:", backup)

# Private key for the account
sk = mnemonic.to_private_key(mn)

# Sign the transaction
signed_tx = txn.sign(sk)

# Debugging
#print(dir(algod_client.send_transaction()))

try:
    tx_confirm = algod_client.send_transaction(signed_tx, headers={'content-type': 'application/x-binary'})
    print(tx_confirm)
except Exception as e:
    print(e)
