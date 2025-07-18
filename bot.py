import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_IDS
from database import AsyncSessionLocal
from models import User, UserRole
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    tg_id = message.from_user.id
    session = AsyncSessionLocal()

    # Проверка, есть ли пользователь
    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        role = UserRole.admin if tg_id in ADMIN_IDS else UserRole.user
        new_user = User(tg_id=tg_id, role=role)
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
        await message.answer(f"👋 Привет! Ты зарегистрирован как *{role.value}*.")
    else:
        await message.answer(f"👋 С возвращением! Ты уже зарегистрирован.")

    await session.close()

if __name__ == "__main__":
    async def main():
        print("Бот запущен...")
        await dp.start_polling(bot)

    asyncio.run(main())
