Function Signature:
funcsign.py

import hashlib

# Function name and parameter types for earnCarbonCredits
function_name_earn = "earnCarbonCredits"
parameter_types_earn = ["uint256"]

# Concatenate the function name and parameter types
signature_string_earn = f"{function_name_earn}({','.join(parameter_types_earn)})"

# Calculate the Keccak hash (SHA-3) of the signature string
keccak_hash_earn = hashlib.sha3_256(signature_string_earn.encode()).hexdigest()

# Take the first four bytes (8 characters) of the hash as the function signature
function_signature_earn = keccak_hash_earn[:8]

print(f"Function Signature for {function_name_earn}: {function_signature_earn}")

# Function name and parameter types for redeemTokens
function_name_redeem = "redeemTokens"
parameter_types_redeem = ["uint256"]

# Concatenate the function name and parameter types
signature_string_redeem = f"{function_name_redeem}({','.join(parameter_types_redeem)})"

# Calculate the Keccak hash (SHA-3) of the signature string
keccak_hash_redeem = hashlib.sha3_256(signature_string_redeem.encode()).hexdigest()

# Take the first four bytes (8 characters) of the hash as the function signature
function_signature_redeem = keccak_hash_redeem[:8]

print(f"Function Signature for {function_name_redeem}: {function_signature_redeem}")
