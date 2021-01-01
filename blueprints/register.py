import datetime

from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter,
)

from sql import crud
from utils.constants import MENU

reg_router = DefaultRouter()


@simple_bot_message_handler(reg_router, PayloadFilter({"command": "yes"}))
async def confirm_yes(event: SimpleBotEvent):
    # Подтверждение аккаунта.
    current_user = event["current_user"]
    if crud.check_pet_name(current_user.pet_id):
        return "Этот аккаунт уже привязан другим пользователем. " \
               "Если он принадлежит Вам, то напишите " \
               "[id496579832|администрации]."
    crud.update_user_status(current_user.user_id, "ok")
    await event.answer(message="Аккаунт привязан!",
                       keyboard=MENU.get_keyboard())


@simple_bot_message_handler(reg_router, PayloadFilter({"command": "not"}))
async def confirm_not(event: SimpleBotEvent):
    # Отмена подтверждения.
    current_user = event["current_user"]
    crud.update_user_status(current_user.user_id, "waiting_name")
    await event.answer(message="Отправьте свой ник/id заново.",
                       keyboard=MENU.get_empty_keyboard())