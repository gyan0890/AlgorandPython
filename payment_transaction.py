import json
from algosdk.v2client import algod
from algosdk import account, mnemonic, kmd
from algosdk.future import transaction
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn


algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = ""
headers = {
    "X-API-Key": "YOUR API KEY HERE",
}


# Initialize an algod client
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

# Add your account mnemonics here
mnemonic1 = "Account 1 Mnemonic"
mnemonic2 = "Account 2 Mnemonic"
mnemonic3 = "Account 3 Mnemonic"

# # For ease of reference, add account public and private keys to
# # an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1


sender_address = accounts[1]['pk']
params = algod_client.suggested_params()
params.flat_fee = True
params.fee = 1000
send_amount = 10
receiver_address = accounts[2]['pk']

txn = transaction.PaymentTxn(sender_address, params, receiver_address, send_amount)
signed_txn = txn.sign(accounts[1]['sk'])
txid = algod_client.send_transaction(signed_txn)
print("Transaction ID is: ", txid)

#Waiting for transaction confirmation
def wait_for_confirmation(client, txid):
    #     """
#     Utility function to wait until the transaction is
#     confirmed before proceeding.
#     """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

print(wait_for_confirmation(algod_client, txid))
