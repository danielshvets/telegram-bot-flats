from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
import asyncio
import config_routes

load_dotenv()
TOKEN = getenv('TOKEN')

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(config_routes.router_config)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bot was stopped')