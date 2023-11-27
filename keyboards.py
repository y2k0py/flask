from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

on_near_regions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ввімкнути", callback_data='turn_on_near_regions')
        ]
    ]
)
off_near_regions = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вимкнути", callback_data='turn_off_near_regions')
    ]
])



