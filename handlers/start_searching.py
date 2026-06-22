from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from FlatFilter import FlatFilter
from keyboards import get_offer_type_keyboard, get_rooms_keyboard, get_housing_stock_keyboard, get_selection_keyboard
from parsing.request999 import get_response
from parsing.normalizer import normalize
import requests

router = Router()


@router.message(Command("start_searching"))
@router.message(F.text == 'Поиск по квартирам')
async def start_searching(message: Message, state: FSMContext):
    await state.update_data(offer_type=[])
    await state.set_state(FlatFilter.offer_type)
    await message.answer(
        "Введите тип предложения",
        reply_markup=get_offer_type_keyboard([])
    )


@router.callback_query(FlatFilter.offer_type)
async def offer_type_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("offer_type", [])

    if callback.data == "sell":
        if "sell" in selected:
            selected.remove("sell")
        else:
            selected.append("sell")

    elif callback.data == "rent":
        if "rent" in selected:
            selected.remove("rent")
        else:
            selected.append("rent")

    elif callback.data == "next":
        await state.set_state(FlatFilter.rooms_amount)
        await callback.message.edit_text("Выберите комнаты", reply_markup=get_rooms_keyboard([]))
        await callback.answer()
        return

    await state.update_data(offer_type=selected)
    await callback.message.edit_reply_markup(reply_markup=get_offer_type_keyboard(selected))
    await callback.answer()


@router.callback_query(FlatFilter.rooms_amount)
async def rooms_amount_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("rooms_amount", [])

    if callback.data in ["aroom", "one_room_Flat", "two_rooms_flat", "three_rooms_flat"]:
        if callback.data in selected:
            selected.remove(callback.data)
        else:
            selected.append(callback.data)

        await state.update_data(rooms_amount=selected)
        await callback.message.edit_reply_markup(reply_markup=get_rooms_keyboard(selected))

    elif callback.data == "next_rooms":
        await state.set_state(FlatFilter.housing_stock)
        await callback.message.edit_text(
            "Выберите тип жилья",
            reply_markup=get_housing_stock_keyboard([])
        )

    await callback.answer()


@router.callback_query(FlatFilter.housing_stock)
async def housing_stock_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("housing_stock", [])

    if callback.data in ["new", "secondary"]:
        if callback.data in selected:
            selected.remove(callback.data)
        else:
            selected.append(callback.data)

        await state.update_data(housing_stock=selected)
        await callback.message.edit_reply_markup(reply_markup=get_housing_stock_keyboard(selected))

    elif callback.data == "next_stock":
        final_data = await state.get_data()

        response = get_response(final_data)
        flats = normalize(response)

        if not flats:
            await callback.message.edit_text("Ничего не найдено")
            await state.clear()
            await callback.answer()
            return

        await state.update_data(flats=flats, current_index=0)

        flat = flats[0]
        await callback.message.delete()

        caption = (
            f"🏠 {flat['title']}\n\n"
            f"💰 Цена: {flat['price']}\n"
            f"📅 Дата: {flat['date']}"
        )

        has_photo = False
        try:
            r = requests.get(flat["image"], timeout=10)
            if r.status_code == 200:
                await callback.message.answer_photo(
                    photo=BufferedInputFile(r.content, filename="flat.jpg"),
                    caption=caption,
                    reply_markup=get_selection_keyboard(1, len(flats), flat["link"])
                )
                has_photo = True
        except Exception as e:
            print(e)

        if not has_photo:
            await callback.message.answer(
                caption,
                reply_markup=get_selection_keyboard(1, len(flats), flat["link"])
            )

        await state.update_data(has_photo=has_photo)
        await state.set_state(FlatFilter.show_results)

    await callback.answer()


@router.callback_query(
    FlatFilter.show_results,
    F.data.in_(["previous", "next"])
)
async def navigate_results(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    flats = data["flats"]
    index = data["current_index"]
    has_photo = data.get("has_photo", True)

    if callback.data == "next":
        index = (index + 1) % len(flats)
    else:
        index = (index - 1) % len(flats)

    await state.update_data(current_index=index)

    flat = flats[index]

    new_caption = (
        f"🏠 {flat['title']}\n\n"
        f"💰 Цена: {flat['price']}\n"
        f"📅 {flat['date']}"
    )

    keyboard = get_selection_keyboard(index + 1, len(flats), flat["link"])

    if has_photo:
        await callback.message.edit_caption(caption=new_caption, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text=new_caption, reply_markup=keyboard)

    await callback.answer()