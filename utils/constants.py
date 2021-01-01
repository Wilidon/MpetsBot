from vkwave.bots import Keyboard, ButtonColor

MENU = Keyboard()
MENU.add_text_button(text="Личные задания", payload={"command": "user_tasks"},
                     color=ButtonColor.SECONDARY)
MENU.add_text_button(text="Клубные задания", payload={"command": "club_tasks"},
                     color=ButtonColor.SECONDARY)
MENU.add_row()
MENU.add_text_button(text="Рейтинг", payload={"command": "user_rating"},
                     color=ButtonColor.SECONDARY)
MENU.add_text_button(text="Рейтинг", payload={"command": "club_rating"},
                     color=ButtonColor.SECONDARY)
MENU.add_row()
MENU.add_text_button(text="🧸 Профиль", payload={"command": "profile"},
                     color=ButtonColor.POSITIVE)
MENU.add_text_button(text="🎈 Клуб", payload={"command": "club"},
                     color=ButtonColor.POSITIVE)

CONFIRMATION = Keyboard()
CONFIRMATION.add_text_button(text="Да!", payload={"command": "yes"},
                             color=ButtonColor.POSITIVE)
CONFIRMATION.add_text_button(text="Нет!", payload={"command": "not"},
                             color=ButtonColor.NEGATIVE)

SHOP_1 = Keyboard()
SHOP_1.add_text_button(text="400 монет", payload={"command": "400coin"},
                       color=ButtonColor.POSITIVE)
SHOP_1.add_text_button(text="2⚙️(волш.)",
                       payload={"command": "2gears"},
                       color=ButtonColor.POSITIVE)
SHOP_1.add_text_button(text="25 ангелов",
                       payload={"command": "25angels"},
                       color=ButtonColor.POSITIVE)
SHOP_1.add_row()
SHOP_1.add_text_button(text="Назад",
                       payload={"command": "menu"},
                       color=ButtonColor.SECONDARY)


SHOP_2 = Keyboard()
SHOP_2.add_text_button(text="аватарка", payload={"command": "avatar"},
                       color=ButtonColor.POSITIVE)
SHOP_2.add_text_button(text="35 серебра",
                       payload={"command": "35silver"},
                       color=ButtonColor.POSITIVE)
SHOP_2.add_text_button(text="4 монетки удачи",
                       payload={"command": "4luckycoins"},
                       color=ButtonColor.POSITIVE)
SHOP_2.add_row()
SHOP_2.add_text_button(text="Назад",
                       payload={"command": "menu"},
                       color=ButtonColor.SECONDARY)


SHOP_3 = Keyboard()
SHOP_3.add_text_button(text="600 монет", payload={"command": "600coins"},
                       color=ButtonColor.POSITIVE)
SHOP_3.add_text_button(text="16m ❣️",
                       payload={"command": "16mhearts"},
                       color=ButtonColor.POSITIVE)
SHOP_3.add_text_button(text="6⚙️(обыч.)",
                       payload={"command": "6gears"},
                       color=ButtonColor.POSITIVE)
SHOP_3.add_row()
SHOP_3.add_text_button(text="Назад",
                       payload={"command": "menu"},
                       color=ButtonColor.SECONDARY)