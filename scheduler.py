import asyncio
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from database import get_user, calculate_weeks_left, async_session
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

scheduler = AsyncIOScheduler()

async def send_weekly(): 
    async with async_session() as session:
        result = await session.execute('SELECT user_id, birth_date FROM users')
        users = result.all()
        
        for user_id, birth_date in users:
             weeks_lived, weeks_left = calculate_weeks_left(birth_date)
             message = (
                f"Data birth: {birth_date}\n"
                f"You leaved: {weeks_lived}\n"
                f"Ostalos: {weeks_left}"
             )
             
             await bot.send_message(user_id, message)
             
# scheduler.add_job(send_weekly, "cron", day_of_week="sat", hour=10, minute=0)
scheduler.add_job(send_weekly, "interval", minutes=1)


def start_scheduler() :
    scheduler.start()