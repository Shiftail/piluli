from aiogram import Dispatcher
from aiogram.types import (
    Message, KeyboardButton, ReplyKeyboardMarkup,
    WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
)
from config import WEBAPP_URL

def register_handlers(dp: Dispatcher):
    @dp.message()
    async def handle_all(message: Message):
        if message.text == "/start":
            # Обычная клавиатура (reply)
            reply_kb = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="Открыть WebApp (Reply)",
                            web_app=WebAppInfo(url=WEBAPP_URL)
                        )
                    ]
                ],
                resize_keyboard=True
            )

            # Инлайн-клавиатура
            inline_kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Открыть WebApp (Inline)",
                            web_app=WebAppInfo(url=WEBAPP_URL)
                        )
                    ]
                ]
            )

            await message.answer("Открывай мини-приложение через обычную клавиатуру", reply_markup=reply_kb)
            await message.answer("Или через инлайн-кнопку 👇", reply_markup=inline_kb)

        elif message.web_app_data:
            await message.answer(f"Получены данные: {message.web_app_data.data}")
