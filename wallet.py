from web3 import Web3
from eth_account import Account
from loguru import logger
from utils import USER_AGENTS
from random import choice
w3 = Web3(Web3.HTTPProvider('https://lisk.drpc.org'))

seeds_file = './seeds.txt'

class Wallet:
    def __init__(self, 
                 seed: str,
                 proxy: str,
                 address: str,
                 to_token: str,
                 from_token: str,
                 user_agent: str,
                 balance: int
                 ):
        
        self.seed = seed
        self.proxy = proxy
        self.address = address
        self.to_token = to_token
        self.from_token = from_token
        self.user_agent = user_agent
        self.balance = balance

    def __str__(self):
        return (
            f"seed = {self.seed}\n"
            f"proxy = {self.proxy}\n"
            f"address = {self.address}\n"
            f"to_token = {self.to_token}\n"
            f"from_token = {self.from_token}"
            f"user_agent = {self.user_agent}"
        )

if not w3.is_connected():
    logger.error(f"Error connecting to blockchain")
    exit()

Account.enable_unaudited_hdwallet_features()

WALLETS = []

def create_wallets() -> list[Wallet]:
    with open(seeds_file, 'r') as file:
        seeds: list[str] = file.readlines()

    for seed in seeds:
        seed = seed.strip()
        
        account = Account.from_mnemonic(seed)
        address = account.address 

        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')
        user_agent = choice(USER_AGENTS)
        
        wallet = Wallet(
            seed=seed,
            proxy='',
            address=address,
            to_token='',
            from_token='',
            balance=balance,
            user_agent=user_agent
                )
        WALLETS.append(wallet)

create_wallets()
