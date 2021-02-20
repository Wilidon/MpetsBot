from datetime import datetime

from vkwave.bots import Keyboard, ButtonColor


from sql import crud
from utils.constants import shop2, shop3, holiday_1402, holiday_2302


async def get_kb(shop: bool = False, access: int = 0, holiday: int = False):
    MENU = Keyboard()
    if holiday_1402[0] <= holiday <= holiday_1402[1]+1:
        MENU.add_text_button(text="❤️День Святого Валентина",
                             payload={"command": "0214"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
    elif holiday_2302[0] <= holiday <= holiday_2302[1]+1:
        MENU.add_text_button(text="👨‍✈️День защитника Отечества",
                             payload={"command": "0223"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
    MENU.add_text_button(text="🗒 Личные задания",
                         payload={"command": "user_tasks"},
                         color=ButtonColor.SECONDARY)
    MENU.add_text_button(text="🧾 Клубные задания",
                         payload={"command": "club_tasks"},
                         color=ButtonColor.SECONDARY)
    MENU.add_row()
    MENU.add_text_button(text="🏅 Рейтинг",
                         payload={"command": "user_rating"},
                         color=ButtonColor.SECONDARY)
    MENU.add_text_button(text="🎈 Рейтинг",
                         payload={"command": "club_rating"},
                         color=ButtonColor.SECONDARY)
    MENU.add_row()
    MENU.add_text_button(text="🧸 Профиль",
                         payload={"command": "profile"},
                         color=ButtonColor.POSITIVE)
    MENU.add_text_button(text="🏡 Клуб",
                         payload={"command": "club"},
                         color=ButtonColor.POSITIVE)
    if shop:
        MENU.add_row()
        MENU.add_text_button(text="🏪 Магазин", payload={"command": "shop"},
                             color=ButtonColor.POSITIVE)
    if access >= 3:
        MENU.add_row()
        MENU.add_text_button(text="🌐 Рейтинг игроков",
                             payload={"command": "rating_user_tasks"},
                             color=ButtonColor.POSITIVE)
        MENU.add_text_button(text="🌐 Рейтинг клубов",
                             payload={"command": "rating_club_tasks"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
        MENU.add_text_button(text="🌐 Призы игроков",
                             payload={"command": "user_items"},
                             color=ButtonColor.POSITIVE)
        MENU.add_text_button(text="🌐 Призы клубов",
                             payload={"command": "club_items"},
                             color=ButtonColor.POSITIVE)
    return MENU


CONFIRMATION = Keyboard()
CONFIRMATION.add_text_button(text="Да!", payload={"command": "yes"},
                             color=ButtonColor.POSITIVE)
CONFIRMATION.add_text_button(text="Нет!", payload={"command": "not"},
                             color=ButtonColor.NEGATIVE)

SHOP_1 = Keyboard()
SHOP_1.add_text_button(text="300 монет",
                       payload={"command": "item1"},
                       color=ButtonColor.POSITIVE)
SHOP_1.add_text_button(text="2⚙️(волш.)",
                       payload={"command": "item2"},
                       color=ButtonColor.POSITIVE)
SHOP_1.add_text_button(text="20 ангелов",
                       payload={"command": "item3"},
                       color=ButtonColor.POSITIVE)
SHOP_1.add_row()
SHOP_1.add_text_button(text="Назад",
                       payload={"command": "menu"},
                       color=ButtonColor.SECONDARY)


def get_shop_2(item_ids: list):
    SHOP_2 = Keyboard()
    if not (1 in item_ids):
        SHOP_2.add_text_button(text=shop2["item1"],
                               payload={"command": "item1"},
                               color=ButtonColor.POSITIVE)
    if not (2 in item_ids):
        SHOP_2.add_text_button(text=shop2["item2"],
                               payload={"command": "item2"},
                               color=ButtonColor.POSITIVE)
    SHOP_2.add_row()
    if not (3 in item_ids):
        SHOP_2.add_text_button(text=shop2["item3"],
                               payload={"command": "item3"},
                               color=ButtonColor.POSITIVE)
    if not (4 in item_ids):
        SHOP_2.add_text_button(text=shop2["item4"],
                               payload={"command": "item4"},
                               color=ButtonColor.POSITIVE)
    SHOP_2.add_row()
    SHOP_2.add_text_button(text="Назад",
                           payload={"command": "menu"},
                           color=ButtonColor.SECONDARY)
    return SHOP_2


def get_shop_3(item_ids: list):
    SHOP_3 = Keyboard()
    if not (1 in item_ids):
        SHOP_3.add_text_button(text=shop3["item1"],
                               payload={"command": "item1"},
                               color=ButtonColor.POSITIVE)
    if not (2 in item_ids):
        SHOP_3.add_text_button(text=shop3["item2"],
                               payload={"command": "item2"},
                               color=ButtonColor.POSITIVE)
    if not (3 in item_ids):
        SHOP_3.add_text_button(text=shop3["item3"],
                               payload={"command": "item3"},
                               color=ButtonColor.POSITIVE)
    SHOP_3.add_row()
    if not (4 in item_ids):
        SHOP_3.add_text_button(text=shop3["item4"],
                               payload={"command": "item4"},
                               color=ButtonColor.POSITIVE)
    if not (5 in item_ids):
        SHOP_3.add_text_button(text=shop3["item5"],
                               payload={"command": "item5"},
                               color=ButtonColor.POSITIVE)
    if not (6 in item_ids):
        SHOP_3.add_text_button(text=shop3["item6"],
                               payload={"command": "item6"},
                               color=ButtonColor.POSITIVE)
    SHOP_3.add_row()
    SHOP_3.add_text_button(text="Назад",
                           payload={"command": "menu"},
                           color=ButtonColor.SECONDARY)
    return SHOP_3


async def menu(user, event, message="Меню", holiday=False):
    today = int(datetime.today().strftime("%m%d"))
    items = crud.get_user_item(user.user_id, "shop_%")
    if items:
        keyboard = await get_kb(shop=True, access=user.access, holiday=today)
        await event.answer(message=message, keyboard=keyboard.get_keyboard())
    else:
        keyboard = await get_kb(access=user.access, holiday=today)
        await event.answer(message=message, keyboard=keyboard.get_keyboard())
