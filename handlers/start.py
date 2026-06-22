from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from FlatFilter import FlatFilter
from keyboards import get_main_reply_keyboard

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer('Привет! Этот бот призван помочь тебе с выбором и поиском жилья в Кишиневе!\n\n' +
                         'Основные команды для работы с ботом:\n\n'+
                         '/about - выводит информацию о создателе\n'+
                         '/start_searching - Поиск квартирам\n'+
                         '/botinfo - информация о боте'
                         , reply_markup=get_main_reply_keyboard())
    
@router.message(Command("about"))
@router.message(F.text == 'О нас')
async def about(message: Message):
    await message.answer('hello!', reply_markup=get_main_reply_keyboard())

@router.message(Command("botinfo"))
@router.message(F.text == 'Информация о боте')
async def botinfo(message: Message):
    await message.answer('hello!', reply_markup=get_main_reply_keyboard())