import asyncio

from aiogram import Bot, Dispatcher, executor, types
from config import token
from config import id
from main import check_update
from aiogram.utils.markdown import hlink, hbold


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.reply("погнали")


async def updates_every_minute():
    while True:
        new_accounts = check_update()

        if len(new_accounts) >= 1:
            await bot.send_message(id, 'Обновления:')
            for k, v in new_accounts.items():
                updates = f"{hlink(v['description'], v['link'])}\n" \
                          f"{hbold(v['price'])}"

                await bot.send_message(id, updates)
        else:
            pass

        await asyncio.sleep(60)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(updates_every_minute())
    executor.start_polling(dp)