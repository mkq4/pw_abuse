from web3 import Web3
from eth_account import Account
from loguru import logger
from utils import USER_AGENTS, parse_proxy
from random import choice


w3 = Web3(Web3.HTTPProvider('https://lisk.drpc.org'))

seeds_file = 'data/seeds.txt'
proxy_file = 'data/proxy.txt'

class Wallet:
    def __init__(self, 
                 seed: str,
                 proxy: str,
                 address: str,
                 user_agent: str,
                 balance: int
                 ):
        
        self.seed = seed
        self.proxy = proxy
        self.address = address
        self.user_agent = user_agent
        self.balance = balance

    def __str__(self):
        return (
            f"seed = {self.seed}\n"
            f"proxy = {self.proxy}\n"
            f"address = {self.address}\n"
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

    with open(proxy_file, 'r') as file:
        proxies = [proxy.strip() for proxy in file.readlines()]
    new_proxies = []
    for proxy in proxies:
        new_proxy = parse_proxy(proxy)
        new_proxies.append(new_proxy)

    print(new_proxies)

    proxy_seed_pairs = list(zip(new_proxies, seeds))

    for proxy, seed in proxy_seed_pairs:
        account = Account.from_mnemonic(seed)
        address = account.address

        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')

        user_agent = choice(USER_AGENTS)

        wallet = Wallet(
            seed=seed,
            proxy=proxy,
            address=address,
            balance=balance,
            user_agent=user_agent
        )
        WALLETS.append(wallet)

create_wallets()
