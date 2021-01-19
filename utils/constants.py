from vkwave.bots import Keyboard, ButtonColor

from sql import crud

MENU = Keyboard()
MENU.add_text_button(text="🗒 Личные задания",
                     payload={"command": "user_tasks"},
                     color=ButtonColor.SECONDARY)
MENU.add_text_button(text="🧾 Клубные задания",
                     payload={"command": "club_tasks"},
                     color=ButtonColor.SECONDARY)
MENU.add_row()
MENU.add_text_button(text="🏮 Рейтинг",
                     payload={"command": "user_rating"},
                     color=ButtonColor.SECONDARY)
MENU.add_text_button(text="🏵 Рейтинг",
                     payload={"command": "club_rating"},
                     color=ButtonColor.SECONDARY)
MENU.add_row()
MENU.add_text_button(text="🧸 Профиль",
                     payload={"command": "profile"},
                     color=ButtonColor.POSITIVE)
MENU.add_text_button(text="🎈 Клуб",
                     payload={"command": "club"},
                     color=ButtonColor.POSITIVE)

MENU_S = Keyboard()
MENU_S.add_text_button(text="🗒 Личные задания",
                       payload={"command": "user_tasks"},
                       color=ButtonColor.SECONDARY)
MENU_S.add_text_button(text="🧾 Клубные задания",
                       payload={"command": "club_tasks"},
                       color=ButtonColor.SECONDARY)
MENU_S.add_row()
MENU_S.add_text_button(text="🏮 Рейтинг", payload={"command": "user_rating"},
                       color=ButtonColor.SECONDARY)
MENU_S.add_text_button(text="🏵 Рейтинг", payload={"command": "club_rating"},
                       color=ButtonColor.SECONDARY)
MENU_S.add_row()
MENU_S.add_text_button(text="🧸 Профиль", payload={"command": "profile"},
                       color=ButtonColor.SECONDARY)
MENU_S.add_text_button(text="🎈 Клуб", payload={"command": "club"},
                       color=ButtonColor.SECONDARY)
MENU_S.add_row()
MENU_S.add_text_button(text="🏪 Магазин", payload={"command": "shop"},
                       color=ButtonColor.POSITIVE)

ADMIN_MENU = Keyboard()
ADMIN_MENU.add_text_button(text="🗒 Личные задания",
                           payload={"command": "user_tasks"},
                           color=ButtonColor.SECONDARY)
ADMIN_MENU.add_text_button(text="🧾 Клубные задания",
                           payload={"command": "club_tasks"},
                           color=ButtonColor.SECONDARY)
ADMIN_MENU.add_row()
ADMIN_MENU.add_text_button(text="🏮 Рейтинг", payload={"command": "user_rating"},
                           color=ButtonColor.SECONDARY)
ADMIN_MENU.add_text_button(text="🏵 Рейтинг", payload={"command": "club_rating"},
                           color=ButtonColor.SECONDARY)
ADMIN_MENU.add_row()
ADMIN_MENU.add_text_button(text="🧸 Профиль", payload={"command": "profile"},
                           color=ButtonColor.SECONDARY)
ADMIN_MENU.add_text_button(text="🎈 Клуб", payload={"command": "club"},
                           color=ButtonColor.SECONDARY)
ADMIN_MENU.add_row()
ADMIN_MENU.add_text_button(text="🌐 Рейтинг игроков",
                           payload={"command": "rating_user_tasks"},
                           color=ButtonColor.POSITIVE)
ADMIN_MENU.add_text_button(text="🌐 Рейтинг клубов",
                           payload={"command": "rating_club_tasks"},
                           color=ButtonColor.POSITIVE)
ADMIN_MENU.add_row()
ADMIN_MENU.add_text_button(text="🌐 Призы игроков",
                           payload={"command": "user_items"},
                           color=ButtonColor.POSITIVE)
ADMIN_MENU.add_text_button(text="🌐 Призы клубов",
                           payload={"command": "club_items"},
                           color=ButtonColor.POSITIVE)

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
        SHOP_2.add_text_button(text="17 серебра",
                               payload={"command": "item1"},
                               color=ButtonColor.POSITIVE)
    if not (2 in item_ids):
        SHOP_2.add_text_button(text="2m ❤️",
                               payload={"command": "item2"},
                               color=ButtonColor.POSITIVE)
    if not (3 in item_ids):
        SHOP_2.add_text_button(text="2 монетки удачи",
                               payload={"command": "item3"},
                               color=ButtonColor.POSITIVE)
    if not (4 in item_ids):
        SHOP_2.add_text_button(text="13 ангелов",
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
        SHOP_3.add_text_button(text="600 монет",
                               payload={"command": "item1"},
                               color=ButtonColor.POSITIVE)
    if not (2 in item_ids):
        SHOP_3.add_text_button(text="16m ❣️",
                               payload={"command": "item2"},
                               color=ButtonColor.POSITIVE)
    if not (3 in item_ids):
        SHOP_3.add_text_button(text="6⚙️(обыч.)",
                               payload={"command": "item3"},
                               color=ButtonColor.POSITIVE)
    SHOP_3.add_row()
    SHOP_3.add_text_button(text="Назад",
                           payload={"command": "menu"},
                           color=ButtonColor.SECONDARY)
    return SHOP_3


async def menu(user, event, message="Меню"):
    items = crud.get_user_item(user.user_id, "shop_%")
    if items:
        await event.answer(message=message, keyboard=MENU_S.get_keyboard())
    else:
        if user.access >= 1:
            await event.answer(message=message, keyboard=ADMIN_MENU.get_keyboard())
        else:
            await event.answer(message=message, keyboard=MENU.get_keyboard())
