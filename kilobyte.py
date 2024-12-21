#────────────────────────────── ✦ ──────────────────────────────
#Created by Ivan Shcherbakov (github: https://github.com/ivansherbakov9) (telegram: https://t.me/Gunner951)
#────────────────────────────── ✦ ──────────────────────────────
import os
import json
import asyncio
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatAdministratorRights
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '*'
POINTS_FILE = "user_points.json"
AUTHORIZED_USERS_FILE = "authorized_users.json"
ADMIN_ID = 1808806022
CREATOR_ID = 1808806022 #MIT License

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_points = {}
authorized_users = set()

def get_rank(points):
    if points > 20:
        return "♛"
    elif points > 10:
        return "♜"
    else:
        return "♝"

def load_points():
    if os.path.exists(POINTS_FILE):
        try:
            with open(POINTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                data = {int(k): v for k, v in data.items()}
                return data
        except json.JSONDecodeError:
            print("Error: json.JSONDecodeError:Ошибка чтения файла с баллами. Начинаем с пустого списка.")
    return dict()

def save_points():
    with open(POINTS_FILE, "w", encoding="utf-8") as f:
        data_to_save = {str(k): v for k, v in user_points.items()}
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

def load_authorized_users():
    if os.path.exists(AUTHORIZED_USERS_FILE):
        try:
            with open(AUTHORIZED_USERS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print("Error: json.JSONDecodeError:Ошибка чтения файла с авторизованными пользователями. Начинаем с пустого списка.")
    return set()

def save_authorized_users():
    with open(AUTHORIZED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(authorized_users), f, ensure_ascii=False, indent=4)

user_points = load_points()
authorized_users = load_authorized_users()

print(f"INFO: Загруженные баллы пользователей:\n{user_points}")
print(f"INFO: Загруженные авторизованные пользователи:\n{authorized_users}")

@dp.message_handler(commands=["pi", "points_info", "ip", "info_points"])
async def info(message: types.Message):
    msg = await message.reply(
        "❁| Система баллов(/pi).\n"
        "   Баллы знатока - это число, которое показывает насколько человек разбирается в данной области.\n"
        "   Чем больше число после слова 'Знаток:', тем больше можно полагаться на советы и ответы человека.\n"
        "Существуют следующие ранги репутации:\n"
        "   ♝ - Начальный ранг.(Знаток:1-10)\n"
        "   ♜ - Продвинутый ранг.(Знаток:11-20)\n"
        "   ♛ - Профессиональный ранг.(Знаток:21+)\n"
        "Условия:\n"
        "   -Балл дается за помощь или ответ, который помог найти решение вашего вопроса на тему AI/ML/DL.\n"
        "   -Вы можете давать баллы, только после того, как пройдете верификацию - /v .\n"
        "   -Если вы будете замечены в не справедливом получении или начислении другому пользователю баллов, вы будете наказаны.\n"
        "Команды:\n"
        "/pi - получить информацию о системе баллов.\n"
        "/v - пройти верификацию.\n"
        "/pa - добавить балл участнику, ответив на его сообщение.\n"
        "/pb - посмотреть свое кол-во баллов.\n"
    )

    await asyncio.sleep(120)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Error: Не удалось удалить сообщение. Ошибка: {e}")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось удалить сообщение. Ошибка: {e}")

@dp.message_handler(commands=["v"])
async def verification(message: types.Message):
    user_id = message.from_user.id

    if user_id not in authorized_users:
        authorized_users.add(user_id)
        save_authorized_users()

    msg = await message.reply("Верификация прошла успешно. Спасибо. (/pi)")

    await asyncio.sleep(5)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Error: Не удалось удалить сообщение. Ошибка: {e}")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось удалить сообщение. Ошибка: {e}")

@dp.message_handler(commands=["pa", "point_add", "ap", "add_point", "дб", "добавить_балл"])
async def add_points(message: types.Message):
    if not message.reply_to_message:
        msg = await message.reply("Чтобы добавить балл, ответьте на сообщение человека. (/pi)")

        await asyncio.sleep(5)

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            print(f"Error: Не удалось удалить сообщение. Ошибка: {e}")
            await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось удалить сообщение. Ошибка: {e}")
        
        return

    target_user_id = message.reply_to_message.from_user.id
    
    if message.from_user.id not in authorized_users:
        msg = await message.reply("Вы не можете выдавать баллы, пока не пройдете верификацию - /v.")

        await asyncio.sleep(5)

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            print(f"Error: Не удалось удалить сообщение. Ошибка: {e}")
            await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось удалить сообщение. Ошибка: {e}")
            
        return

    if user_points.get(target_user_id) is not None:
        user_points[target_user_id] += 1
    else:
        user_points[target_user_id] = 1    

    try:
        member_status = await bot.get_chat_member(message.chat.id, target_user_id)
        if member_status.status not in ['creator', 'владелец', 'points sys.(/pi)', 'Владелец', 'админ']:
            await bot.promote_chat_member(
                chat_id=message.chat.id,
                user_id=target_user_id,
                can_manage_chat=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )

    except Exception as e:
        print(f"Error: Не удалось выдать балл. Ошибка: {e}")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось выдать балл. Ошибка: {e}")
        return

    prefix = f"{(get_rank(user_points[target_user_id])) if target_user_id != CREATOR_ID else '✦'}Знаток: {user_points[target_user_id]}"
    try:
        await bot.set_chat_administrator_custom_title(
            chat_id=message.chat.id,
            user_id=target_user_id,
            custom_title=prefix
        )
    except Exception as e:
        print(f"Error: Не удалось выдать балл. Ошибка: {e}")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось выдать балл. Ошибка: {e}")
        return

    save_points()

    msg = await message.reply(f"Пользователю успешно добавлен 1 балл. Спасибо. (/pi)")

    await asyncio.sleep(5)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Error: Не удалось удалить сообщение. Ошибка: {e}")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nError: Не удалось удалить сообщение. Ошибка: {e}")

@dp.message_handler(commands=["pb"])
async def points_balance(message: types.Message):
    user_id = message.from_user.id

    if user_points.get(user_id) is not None:
        user_balance = user_points[user_id]
    else:
        user_balance = 0
    msg = await message.reply(f"Ваш профиль(/pi):\n{get_rank(user_balance)}Знаток: {user_balance}")

    await asyncio.sleep(7)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Error: Не удалось удалить сообщение. Ошибка: {e}")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error: Не удалось удалить сообщение. Ошибка: {e}")
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
#────────────────────────────── ✦ ──────────────────────────────
#Created by Ivan Shcherbakov (https://github.com/ivansherbakov9/Points-System-In-TG-Kilobyte)
#────────────────────────────── ✦ ──────────────────────────────
