from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    json_prompt = State()
    image_prompt = State()