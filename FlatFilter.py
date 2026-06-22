from aiogram.fsm.state import StatesGroup, State

class FlatFilter(StatesGroup):
    offer_type = State()
    rooms_amount = State()
    housing_stock = State()
    show_results = State()