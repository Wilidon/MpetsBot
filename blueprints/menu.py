from loguru import logger
from vkwave.bots import DefaultRouter, SimpleBotEvent, \
    simple_bot_message_handler, PayloadFilter, TextContainsFilter

from mpetsapi import MpetsApi
from sql import crud
from keyboards.kb import CONFIRMATION, menu
from utils.constants import user_task_log, club_task_log, collections
from utils.functions import notice

menu_router = DefaultRouter()


@simple_bot_message_handler(menu_router,
                            PayloadFilter({"command": "menu"}))
async def back_menu(event: SimpleBotEvent):
    user = event["current_user"]
    await menu(user, event)


@simple_bot_message_handler(menu_router,
                            TextContainsFilter(
                                ["/report"]))
async def report(event: SimpleBotEvent):
    user = event["current_user"]
    try:
        msg = event.object.object.message.text.split(" ", maxsplit=1)[1]
    except Exception as e:
        msg = "Null"
        await event.answer("Расскажите о своей проблеме!\n\n"
                           "В следующий раз не забудьте указать Вашу проблему сразу:\n"
                           "/report «Доброго времени суток! Что такое коллекции и зачем они нужны?»\n"
                           "Так Ваша проблема будет решена в кратчайшие сроки.")
    text = f"{user.first_name} {user.last_name} ({user.user_id}) нуждается в " \
           f"психологической помощи.\n\n" \
           f"Его сообщение: «{msg}»"
    notice(message=text)


@simple_bot_message_handler(menu_router,
                            TextContainsFilter(
                                ["/logs"]))
async def logs(event: SimpleBotEvent):
    user = event["current_user"]
    user_id = user.user_id
    try:
        msg = event.object.object.message.text.split()
        if len(msg) == 2 and user.access >= 3:
            user_id = int(msg[1])
    except Exception as e:
        pass
    text = "Список последних наград\n\n"
    text += f"✏️ Личные: \n"
    user_log = crud.get_user_task_log(user_id=user_id)
    club_log = crud.get_club_task_log(user_id=user_id)
    collection_log = crud.get_collection_log(user_id=user_id)
    for task in user_log:
        task_name = task.task_name
        if "anketa" in task.task_name:
            task_name = task_name.split("_", maxsplit=1)[0]
        text += f"{user_task_log[task_name]} — {task.tasks} 🌼 и {task.points} 🏅\n"
    text += f"\n🎈Клубные:\n"
    for task in club_log:
        task_name = task.task_name
        if "send_specific_gift_any_player" in task.task_name or \
                "get_gift" in task.task_name or \
                "send_gift_any_player" in task.task_name or \
                "get_random_gift" in task.task_name:
            task_name = task_name.rsplit("_", maxsplit=1)[0]
        text += f"{club_task_log[task_name]} — {task.tasks} 🌼 и {task.points} 🏅\n"
    text += f"\n🧩 Коллекции: \n"
    for collection in collection_log:
        collection_icon = collections[collection.collection_id]['required'][collection.part_id-1]['icon']
        text += f"{collections[collection.collection_id]['name']} — {collection_icon} \n"
    await event.answer(message=text)


@simple_bot_message_handler(menu_router)
async def main(event: SimpleBotEvent):
    # Главное меню, подтверждение аккаунта
    current_user = event["current_user"]
    if current_user.status == 'waiting_name':
        mpets = MpetsApi()
        await mpets.start()
        msg, pet = event.object.object.message.text, None
        # Если игрок отправил свой id, то ищем по id. Если по id найти неудалось, 
        # то пробуем найти еще и по нику.
        if msg.isdigit():
            pet = await mpets.view_profile(pet_id=msg)
            if pet["status"] != "ok":
                pet = await mpets.find_pet(name=msg)
                if pet["status"] == "ok":
                    pet = await mpets.view_profile(pet_id=pet["pet_id"])
        else:
            pet = await mpets.find_pet(name=msg)
            if pet["status"] == "ok":
                pet = await mpets.view_profile(pet_id=pet["pet_id"])
        if pet and pet["status"] != "ok":
            return "Аккаунт не найден. Попробуйте ещё раз!"
        crud.update_user_status(current_user.user_id, "waiting_confirmation")
        if pet["club_id"] == None:  # noqa
            pet["club_id"] == 0  # noqa
        crud.update_user_data(current_user.user_id, pet["pet_id"], pet["name"],
                              pet["club_id"])
        text = f"Ваш аккаунт - {pet['name']}?\n" \
               f"Будьте внимательны, привязывать аккаунт можно только " \
               f"единожды, а его смена невозможна!\n" \
               f"Всё, что Вы купите в магазине, будет начисляться на " \
               f"указанный Вами аккаунт. "
        await event.answer(message=text,
                           keyboard=CONFIRMATION.get_keyboard())
    elif current_user.status == 'newbie':
        crud.update_user_status(current_user.user_id, "waiting_name")
        text = "🙋‍♂️ Привет! Для начала работы с ботом привяжите свой " \
               "аккаунт, отправив нам ID или ник питомца. \n👉 Пример: " \
               "8988812 или Monster\n\n" \
               "❗ Бот находится в стадии бета-тестирования. В процессе " \
               "работы могут возникнуть ошибки. Если Вы обнаружили ошибку, " \
               "то вызовите администрацию в чат командой /report."
        await event.answer(message=text)
    elif current_user.status == 'ok' and \
            event.object.object.message.text.lower() in ("меню", "старт",
                                                         "начать", "початок"):
        await menu(current_user, event)
    else:
        black_list = [485026972, 578062764]
        if current_user.user_id in black_list:
            pass
        else:
            text = f"{current_user.first_name} {current_user.last_name} ({current_user.user_id}) пишет.\n\n" \
                   f"Его сообщение: «{event.object.object.message.text}»"
            notice(message=text)
