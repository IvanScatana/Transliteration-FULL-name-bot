import logging 
import asyncio
import os

from datetime import datetime

from aiogram import Bot, Dispatcher
from handler import router
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token = TOKEN)
dp = Dispatcher()



log_filename = f"bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())