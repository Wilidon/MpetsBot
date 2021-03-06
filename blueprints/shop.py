import json

from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter,
)

from sql import crud
from keyboards.kb import SHOP_1, get_shop_2, get_shop_3, menu
from utils.functions import notice
from utils.constants import shop1, shop2, shop3

shop_router = DefaultRouter()


@simple_bot_message_handler(shop_router,
                            PayloadFilter({"command": "item1"}) |
                            PayloadFilter({"command": "item2"}) |
                            PayloadFilter({"command": "item3"}) |
                            PayloadFilter({"command": "item4"}) |
                            PayloadFilter({"command": "item5"}) |
                            PayloadFilter({"command": "item6"}))
async def choose_item(event: SimpleBotEvent):
    user = event["current_user"]
    try:
        item_id = json.loads(event.object.object.message.payload)["command"]
    except Exception:
        return "Ошибка"
    items = crud.get_user_item(user.user_id, "shop_%")
    for item in items:
        if int(item.score) == 2:
            crud.update_user_itemname(item.id, shop1[item_id],
                                      "В процессе")
            await menu(user=user,
                       event=event,
                       message="Награда будет начислена в течение недели.")
            text = f"Игрок {user.first_name} {user.last_name} | {user.name} " \
                   f"({user.pet_id}) выбрал в магазине: \n" \
                   f"{shop1[item_id]}"
            notice(text)
            break
        elif int(item.score) == 2:
            if item.status == "shop_2":
                shop_id = item_id.split("m")[1]
                crud.update_user_itemname(item.id, shop2[item_id],
                                          f"shop_2.{shop_id}")
                await event.answer(message=f"🏪 Выберите второй предмет",
                                   keyboard=get_shop_2([int(
                                       shop_id)]).get_keyboard())
            elif item.status == "shop_2.1":
                item_name = f"{item.item_name} {shop2[item_id]}"
                crud.update_user_itemname(item.id, item_name,
                                          "В процессе")
                await menu(user, event, "Награда будет начислена в течение "
                                        "недели.")
            elif item.status == "shop_2.2":
                item_name = f"{item.item_name} {shop2[item_id]}"
                crud.update_user_itemname(item.id, item_name,
                                          "В процессе")
                await menu(user, event, "Награда будет начислена в течение "
                                        "недели.")
            elif item.status == "shop_2.3":
                item_name = f"{item.item_name} {shop2[item_id]}"
                crud.update_user_itemname(item.id, item_name,
                                          "В процессе")
                await menu(user, event, "Награда будет начислена в течение "
                                        "недели.")
            elif item.status == "shop_2.4":
                item_name = f"{item.item_name} {shop2[item_id]}"
                crud.update_user_itemname(item.id, item_name,
                                          "В процессе")
                await menu(user, event, "Награда будет начислена в течение "
                                        "недели.")
            break
        elif int(item.score) == 2:
            ids = item.status.split("_3")[1].split(".")[1:]
            ids = [int(i) for i in ids]
            shop_id = item_id.split("m")[1]
            if item.status == "shop_3":
                crud.update_user_itemname(item.id, shop3[item_id],
                                          f"shop_3.{shop_id}")
                await event.answer(message=f"🏪 Выберите второй предмет",
                                   keyboard=get_shop_3([int(
                                       shop_id)]).get_keyboard())
            elif len(ids) == 1:
                item_name = f"{item.item_name} {shop3[item_id]}"
                crud.update_user_itemname(item.id, item_name,
                                          f"{item.status}.{shop_id}")
                ids.append(int(shop_id))
                await event.answer(message=f"🏪 Выберите третий предмет",
                                   keyboard=get_shop_3(ids).get_keyboard())
            elif len(ids) == 2:
                item_name = f"{item.item_name} {shop3[item_id]}"
                crud.update_user_itemname(item.id, item_name,
                                          f"В процессе")
                await menu(user, event, "Награда будет начислена в течение "
                                        "недели.")
            break


@simple_bot_message_handler(shop_router, PayloadFilter({"command": "shop"}))
async def shop(event: SimpleBotEvent):
    current_user = event["current_user"]
    items = crud.get_user_item(current_user.user_id, "shop%")
    for item in items:
        if int(item.score) == 2:
            await event.answer(message=f"🏪 Магазин за {item.score} очков\n"
                                       f"Выберите один приз на выбор",
                               keyboard=SHOP_1.get_keyboard())
            break
        elif int(item.score) == 2:
            if item.status == "shop_2":
                await event.answer(
                    message=f"🏪 Магазин за {item.score} очков\n"
                            f"Выберите два приза на выбор",
                    keyboard=get_shop_2([]).get_keyboard())
            elif item.status == "shop_2.1":
                await event.answer(message=f"🏪 Магазин за {item.score} очков",
                                   keyboard=get_shop_2([1]).get_keyboard())
            elif item.status == "shop_2.2":
                await event.answer(message=f"🏪 Магазин за {item.score} очков",
                                   keyboard=get_shop_2([2]).get_keyboard())
            elif item.status == "shop_2.3":
                await event.answer(message=f"🏪 Магазин за {item.score} очков",
                                   keyboard=get_shop_2([3]).get_keyboard())
            elif item.status == "shop_2.4":
                await event.answer(message=f"🏪 Магазин за {item.score} очков",
                                   keyboard=get_shop_2([4]).get_keyboard())
            break
        elif int(item.score) == 2:
            ids = item.status.split("_3")[1].split(".")[1:]
            ids = [int(i) for i in ids]
            if item.status == "shop_3":
                await event.answer(
                    message=f"🏪 Магазин за {item.score} очков\n"
                            f"Выберите три приза на выбор",
                    keyboard=get_shop_3([]).get_keyboard())
            else:
                await event.answer(message=f"🏪 Магазин за {item.score} очков",
                                   keyboard=get_shop_3(ids).get_keyboard())
            break
