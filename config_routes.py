from aiogram import Router
from handlers import start, start_searching

router_config = Router()

#start_router
router_config.include_router(start.router)

#start_searching
router_config.include_router(start_searching.router)