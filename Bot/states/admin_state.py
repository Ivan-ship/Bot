from aiogram.fsm.state import State, StatesGroup

class AdminState(StatesGroup):
    waiting_tg_id = State()
    waiting_text = State()


