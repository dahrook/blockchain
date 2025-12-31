from web3 import Web3
import json
import hashlib

# -----------------------------
# Step 1: Connect to Hardhat node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Use the first Hardhat account
account = w3.eth.accounts[0]

# Load contract ABI
with open("C:\\Users\\User\\\Desktop\\blockchain_hardhat\\artifacts\\contracts\\Traceability.sol\\Traceability.json") as f:
    abi = json.load(f)["abi"]

# Contract address (from deploy)
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract = w3.eth.contract(address=contract_address, abi=abi)

# -----------------------------
# Step 2: Load LLM trace record from JSON (exported from Colab)
with open("llm_trace_record.json") as f:
    llm_trace_record = json.load(f)

# -----------------------------
# Step 3: Generate SHA-256 hash
def generate_hash(data: dict):
    serialized = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()

llm_hash = generate_hash(llm_trace_record)
print("🔐 LLM HASH:", llm_hash)

# -----------------------------
# Step 4: Store hash on blockchain
tx = contract.functions.storeRecord(
    "ContractXYZ",          # Contract identifier
    "LLM",                  # Type of result
    llm_hash,               # SHA-256 hash
    llm_trace_record["llm_metadata"]["model"]  # Model name
).transact({"from": account})

w3.eth.wait_for_transaction_receipt(tx)
print("✅ LLM hash stored on blockchain")

# -----------------------------
# Step 5: Verify stored records
count = contract.functions.getRecordsCount().call()
print("Total records:", count)

# Fetch all records
for i in range(count):
    record = contract.functions.getRecord(i).call()
    print(f"Record {i}:", record)
