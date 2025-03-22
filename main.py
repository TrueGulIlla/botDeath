import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN
from database import create_tables, add_user, get_user, calculate_weeks_left
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def on_startup(): 
    await create_tables()
    start_scheduler()

@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    birth_date = await get_user(user_id)
    
    if birth_date: 
        weeks_lived, weeks_left = calculate_weeks_left(birth_date)
        await message.answer(
            f"You alrady exist\n"
            f"Data birth: {birth_date}\n"
            f"You leaved: {weeks_lived}\n"
            f"Ostalos: {weeks_left}"
            
        )
    else: 
        await message.answer(f"Hello! Enter your b-date yyyy-mm-dd")
        
        
@dp.message()
async def save_birth_date(message: Message): 
    user_id = message.from_user.id
    birth_date = message.text
    
    try: 
        import datetime
        datetime.datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        await message.answer("No correct data")
        return
    
    await add_user(user_id, birth_date)
    weeks_lived, weeks_left = calculate_weeks_left(birth_date)
    
    await message.answer(
            f"Data birth: {birth_date}\n"
            f"You leaved: {weeks_lived}\n"
            f"Ostalos: {weeks_left}"
            
        )
    
async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
