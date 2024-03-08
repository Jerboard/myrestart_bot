import asyncio
import logging
import sys

from handlers import dp
from init import set_main_menu, bot, DEBUG
from db.base import init_models
from utils.notifications import notifications_scheduler


async def main() -> None:
    await init_models()
    await set_main_menu()
    # await notifications_scheduler ()
    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, filename='log.log')
    asyncio.run(main())
