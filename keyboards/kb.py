import datetime
import time

from vkwave.bots import Keyboard, ButtonColor

from config import get_db
from sql import crud
from utils.collection_handler import check_collected_collection
from utils.constants import shop2, shop3, holiday_1402, holiday_2302, collections, holiday_308, holiday_401


async def get_kb(shop: bool = False, access: int = 0, today: int = False, boss_btn: bool = False):
    MENU = Keyboard()
    db = get_db()
    boss_start = db.get("boss_start")
    boss_end = db.get("boss_end")
    if holiday_1402[0] <= today <= holiday_1402[1]:
        MENU.add_text_button(text="❤️День Святого Валентина",
                             payload={"command": "0214"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
    elif holiday_2302[0] <= today <= holiday_2302[1]:
        MENU.add_text_button(text="👨‍✈️День защитника Отечества",
                             payload={"command": "0223"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
    elif holiday_308[0] <= today <= holiday_308[1]:
        MENU.add_text_button(text="🌹 Международный женский день",
                             payload={"command": "0308"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
    elif holiday_401[0] <= today <= holiday_401[1]:
        MENU.add_text_button(text="❗ Удалить игру",
                             payload={"command": "0401"},
                             color=ButtonColor.POSITIVE)
        MENU.add_row()
    today_date = int(datetime.datetime.today().strftime("%Y%m%d"))
    if boss_start <= today <= boss_end:
        if boss_btn is True:
            MENU.add_text_button(text="🦠 Монстр",
                                 payload={"command": "boss"},
                                 color=ButtonColor.POSITIVE)
            MENU.add_row()
        else:
            MENU.add_text_button(text="🦠 Монстр",
                                 payload={"command": "boss"},
                                 color=ButtonColor.SECONDARY)
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
    MENU.add_row()
    MENU.add_text_button(text="🧩Коллекции ",
                         payload={"command": "collections"},
                         color=ButtonColor.PRIMARY)
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


async def to_collect(user, event, message="Лера, не забудь добавить текст"):
    COLLECTION_KB = Keyboard()
    for collection in collections.items():
        collection_id = collection[0]
        result = await check_collected_collection(user_id=user.user_id,
                                                  collection_id=collection_id)
        if collection_id == 4:
            COLLECTION_KB.add_row()
        if result is False:
            payload = {"command": "collection_id=" + str(collection_id)}
            COLLECTION_KB.add_text_button(text=collection_id,
                                          payload=payload,
                                          color=ButtonColor.SECONDARY)
        else:
            payload = {"command": "collection_id=" + str(collection_id)}
            COLLECTION_KB.add_text_button(text=collection_id,
                                          payload=payload,
                                          color=ButtonColor.POSITIVE)
    COLLECTION_KB.add_row()
    COLLECTION_KB.add_text_button(text="🔽 Назад",
                                  payload={"command": "collections"},
                                  color=ButtonColor.SECONDARY)
    await event.answer(message=message, keyboard=COLLECTION_KB.get_keyboard())


async def collection_kb(user, event, message="Лера, не забудь добавить текст"):
    COLLECTION_KB = Keyboard()
    btn_green = False
    for collection in collections.items():
        collection_id = collection[0]
        result = await check_collected_collection(user_id=user.user_id,
                                                  collection_id=collection_id)
        if result is True:
            btn_green = True
            break
    if btn_green is True:
        COLLECTION_KB.add_text_button(text="Собрать 🧩",
                                      payload={"command": "to_collect"},
                                      color=ButtonColor.POSITIVE)
    else:
        COLLECTION_KB.add_text_button(text="Собрать 🧩",
                                      payload={"command": "to_collect"},
                                      color=ButtonColor.SECONDARY)
    COLLECTION_KB.add_row()
    COLLECTION_KB.add_text_button(text="🔽 Назад",
                                  payload={"command": "menu"},
                                  color=ButtonColor.SECONDARY)
    await event.answer(message=message, keyboard=COLLECTION_KB.get_keyboard())


async def boss_kb(user, event, message="Лера, не забудь добавить текст", btn=False):
    BOSS_KB = Keyboard()
    if btn:
        BOSS_KB.add_text_button(text="⚔️Ударить!",
                                payload={"command": "hit"},
                                color=ButtonColor.POSITIVE)
    else:
        BOSS_KB.add_text_button(text="⚔️Ударить!",
                                payload={"command": "hit"},
                                color=ButtonColor.SECONDARY)
    BOSS_KB.add_row()
    '''if user.access >= 3:
        if boss_amount == 1:
            BOSS_KB.add_text_button(text="Убить!",
                                    payload={"command": "kill1"},
                                    color=ButtonColor.POSITIVE)
            BOSS_KB.add_row()
        if boss_amount == 2:
            BOSS_KB.add_text_button(text="Убить!",
                                    payload={"command": "kill1"},
                                    color=ButtonColor.NEGATIVE)
            BOSS_KB.add_text_button(text="Убить!",
                                    payload={"command": "kill2"},
                                    color=ButtonColor.PRIMARY)
            BOSS_KB.add_row()'''
    BOSS_KB.add_text_button(text="🔽 Назад",
                            payload={"command": "menu"},
                            color=ButtonColor.SECONDARY)
    await event.answer(message=message, keyboard=BOSS_KB.get_keyboard())


async def menu(user, event, message="Меню"):
    today = int(datetime.datetime.today().strftime("%m%d"))
    items = crud.get_user_item(user.user_id, "shop_%")
    btn = True
    user_restart = crud.get_user_restart(user_id=user.user_id)
    if user_restart.time > int(time.time()):
        btn = False
    if items:
        keyboard = await get_kb(shop=True, access=user.access, today=today, boss_btn=btn)
        await event.answer(message=message, keyboard=keyboard.get_keyboard())
    else:
        keyboard = await get_kb(access=user.access, today=today, boss_btn=btn)
        await event.answer(message=message, keyboard=keyboard.get_keyboard())
