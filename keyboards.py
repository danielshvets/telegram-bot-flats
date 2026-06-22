from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from FlatFilter import FlatFilter

#there are keyboards which used for any cases 
def get_main_reply_keyboard():
    keys = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='О нас')],
            [KeyboardButton(text='Поиск по квартирам'), KeyboardButton(text='Информация о боте')]
        ],
        resize_keyboard=True
    )
    return keys

def get_offer_type_keyboard(selected: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'sell' in selected else '☑️'} Продажа",
                    callback_data="sell"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'rent' in selected else '☑️'} Аренда",
                    callback_data="rent"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Дальше",
                    callback_data="next"
                )
            ]
        ]
    )

def get_rooms_keyboard(selected: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'aroom' in selected else '☑️'} Комната",
                    callback_data="aroom"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'one_room_flat' in selected else '☑️'} Однокомнатная квартира",
                    callback_data="one_room_flat"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'two_rooms_flat' in selected else '☑️'} Двухкомнатная квартира",
                    callback_data="two_rooms_flat"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'three_rooms_flat' in selected else '☑️'} Трехкомнатная квартира",
                    callback_data="three_rooms_flat"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Дальше",
                    callback_data="next_rooms"
                )
            ]
        ]
    )

def get_housing_stock_keyboard(selected: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'new' in selected else '☑️'} Новострой",
                    callback_data="new"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{'✅' if 'secondary' in selected else '☑️'} Вторичка",
                    callback_data="secondary"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Дальше",
                    callback_data="next_stock"
                )
            ]
        ]
    )

def get_selection_keyboard(index: int, total: int, link: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text=f"{index}/{total}",
                    callback_data="current"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data="next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔗 Открыть объявление",
                    url=link
                )
            ]
        ]
    )