import asyncio
import random
import config

from metamask.restore_wallet import restore_wallet
from playwright.async_api import async_playwright, expect

from wallet import WALLETS

from loguru import logger


async def main():
    for wallet in WALLETS:
        async with async_playwright() as p:
            proxy = None
            context_kwargs = {
                'headless': False,
                'args': [
                    f"--disable-extensions-except={config.MM_PATH}",
                    f"--load-extension={config.MM_PATH}",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
                'slow_mo': 500,
                'user_agent': wallet.user_agent,
            }

            if proxy:
                context_kwargs['proxy'] = {
                    'server': proxy['server'],
                    'username': proxy['username'],
                    'password': proxy['password'],
                }

            context = await p.chromium.launch_persistent_context('', **context_kwargs)

            await asyncio.sleep(2)
            
            try:
                logger.info(f"Starting wallet - {wallet.address}")
                await restore_wallet(context=context, wallet=wallet)
                # await asyncio.sleep(100000)
            except Exception as e:
                logger.error(f'Error | {e}')
    logger.success('All wallets end 🦍')
    logger.success('🐒 tg - @cryptomakaquich 🐒')


if __name__ == '__main__':
    asyncio.run(main())