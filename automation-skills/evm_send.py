#!/usr/bin/env python3
"""Autonomous EVM transaction signer — used by agent for on-chain actions.

Security model:
    Private key NEVER hardcoded. Loaded from env var or mode-600 file.
    Agent log redacts PK; only env var name is visible in traces.

Usage:
    WAGURI_PK=0x... python3 evm_send.py --to 0x... --value 0.001 --chain base
"""
import argparse
import json
import os

from eth_account import Account
from web3 import Web3

CHAINS = {
    "base": ("https://mainnet.base.org", 8453),
    "ethereum": ("https://eth.llamarpc.com", 1),
    "optimism": ("https://mainnet.optimism.io", 10),
    "arbitrum": ("https://arb1.arbitrum.io/rpc", 42161),
}


def get_pk():
    """Load PK from env (preferred) or mode-600 file."""
    pk = os.environ.get("WAGURI_PK")
    if pk:
        return pk
    pk_file = os.environ.get("WAGURI_PK_FILE", "/home/agent/wallet/wallet_info.txt")
    if os.path.exists(pk_file):
        for line in open(pk_file):
            if line.startswith("PRIVATE_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("No PK in WAGURI_PK env or wallet_info.txt")


def send(to: str, value_eth: float, chain: str = "base", data: str = "0x"):
    rpc, chain_id = CHAINS[chain]
    w3 = Web3(Web3.HTTPProvider(rpc))
    if not w3.is_connected():
        raise RuntimeError(f"Cannot connect to {chain} RPC")

    pk = get_pk()
    acct = Account.from_key(pk)
    print(f"From: {acct.address}")
    print(f"To:   {to}")
    print(f"Chain: {chain} (id={chain_id})")

    nonce = w3.eth.get_transaction_count(acct.address)
    gas_price = w3.eth.gas_price
    value_wei = w3.to_wei(value_eth, "ether")

    tx = {
        "to": w3.to_checksum_address(to),
        "value": value_wei,
        "gas": 21000 if data == "0x" else 200000,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": chain_id,
        "data": data,
    }

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Tx: 0x{tx_hash.hex()}")

    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    print(f"Status: {'success' if receipt.status == 1 else 'failed'}")
    print(f"Block: {receipt.blockNumber}")
    print(f"Gas used: {receipt.gasUsed}")

    return tx_hash.hex()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--value", type=float, required=True)
    parser.add_argument("--chain", default="base", choices=list(CHAINS))
    parser.add_argument("--data", default="0x")
    args = parser.parse_args()

    send(args.to, args.value, args.chain, args.data)
