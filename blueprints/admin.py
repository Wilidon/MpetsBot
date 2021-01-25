import datetime
import time
from random import randint

import pickledb
from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter, MessageArgsFilter, CommandsFilter, TextContainsFilter,
)
from sql import crud
from utils.functions import add_user_points, add_club_points, notice, month, access_name

admin_router = DefaultRouter()


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["+points user", "+points club",
                                 "-points user", "-points club"]),
                            MessageArgsFilter(args_count=2, command_length=2))
async def points(event: SimpleBotEvent):
    # Профиль пользователя
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split()
    if msg[1] == "user":
        if msg[0] == "+points":
            if crud.get_user(int(msg[2])):
                crud.update_user_stats(int(msg[2]), points=int(msg[3]))
                return "✅ Баллы начислены."
            else:
                return "❗ Игрок не найден."
        elif msg[0] == "-points":
            if crud.get_user(int(msg[2])):
                crud.update_user_stats(int(msg[2]), points=-int(msg[3]))
                return "✅ Баллы списаны."
            else:
                return "❗ Игрок не найден."
    if msg[1] == "club":
        if msg[0] == "+points":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), points=int(msg[3]))
                return "✅ Баллы начислены."
            else:
                return "❗ Игрок не найден."
        elif msg[0] == "-points":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), points=-int(msg[3]))
                return "✅ Баллы списаны."
            else:
                return "❗ Игрок не найден."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["+tasks user", "+tasks club",
                                 "-tasks user", "-tasks club"]),
                            MessageArgsFilter(args_count=2, command_length=2))
async def points(event: SimpleBotEvent):
    # Профиль пользователя
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split()
    if msg[1] == "user":
        if msg[0] == "+tasks":
            if crud.get_user(int(msg[2])):
                for i in range(int(msg[3])):
                    await add_user_points(user_id=int(msg[2]), point=False)
                return "✅ Звездочки начислены."
            else:
                return "❗ Игрок не найден."
        elif msg[0] == "-tasks":
            if crud.get_user(int(msg[2])):
                crud.update_user_stats(int(msg[2]), personal_tasks=-int(msg[
                                                                            3]))
                return "✅ Звездочки списаны."
            else:
                return "❗ Игрок не найден."
    if msg[1] == "club":
        if msg[0] == "+tasks":
            if crud.get_club(int(msg[2])):
                for i in range(int(msg[3])):
                    await add_club_points(club_id=int(msg[2]), point=False)
                return "✅ Ёлки начислены."
            else:
                return "❗ Клуб не найден."
        elif msg[0] == "-tasks":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), total_tasks=-int(msg[3]))
                return "✅ Ёлки списаны."
            else:
                return "❗ Клуб не найден."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/user rating", "/club rating"]))
async def points_rating(event: SimpleBotEvent):
    # Рейтинг пользователей
    current_user, counter = event["current_user"], 1
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split()
    if msg[0] == "/user":
        top_users_stats = crud.get_users_stats_order_by_points(limit=None)
        text = "🧑‍ Рейтинг игроков.\n\n"
        if not top_users_stats:
            return "❗ Рейтинг пуст."
        for user_stats in top_users_stats:
            top_user = crud.get_user(user_stats.user_id)
            text += f"{counter}. [id{top_user.user_id}|{top_user.name}] " \
                    f"({top_user.pet_id}) — {user_stats.points} 🏮\n"
            counter += 1
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)
    elif msg[0] == "/club":
        clubs = crud.get_clubs_stats_order_by_points(limit=None)
        text = "🏠 Рейтинг клубов.\n\n"
        if not clubs:
            return "❗ Рейтинг пуст."
        for club_stats in clubs:
            club = crud.get_club(club_stats.club_id)
            text += f"{counter}. {club.name} ({club.club_id}) —" \
                    f" {club_stats.points} 🏵\n"
            counter += 1
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)


@simple_bot_message_handler(admin_router,
                            PayloadFilter({"command": "rating_user_tasks"}))
async def task_rating(event: SimpleBotEvent):
    current_user, counter = event["current_user"], 1
    top_users_stats = crud.get_users_stats_order_by_tasks(limit=None)
    text = "🧑‍ Рейтинг игроков.\n\n"
    if not top_users_stats:
        return "❗ Рейтинг пуст."
    for user_stats in top_users_stats:
        top_user = crud.get_user(user_stats.user_id)
        text += f"{counter}. {top_user.name} — " \
                f"{user_stats.personal_tasks} ⭐\n"
        counter += 1
    if len(text) > 4050:
        await event.answer("Сообщение слишком длинное. Для решение "
                           "проблемы напишите разработчику.")
    else:
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            PayloadFilter({"command": "rating_club_tasks"}))
async def task_rating(event: SimpleBotEvent):
    current_user, counter = event["current_user"], 1
    clubs = crud.get_clubs_stats_order_by_tasks(limit=None)
    text = "🏠 Рейтинг клубов.\n\n"
    if not clubs:
        return "❗ Рейтинг пуст."
    for club_stats in clubs:
        club = crud.get_club(club_stats.club_id)
        text += f"{counter}. {club.name} — {club_stats.total_tasks} 🎄\n"
        counter += 1
    if len(text) > 4050:
        await event.answer("Сообщение слишком длинное. Для решение "
                           "проблемы напишите разработчику.")
    else:
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/user tasks", "/club tasks"]))
async def task_rating(event: SimpleBotEvent):
    # Рейтинг пользователей
    current_user, counter = event["current_user"], 1
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split()
    if msg[0] == "/user":
        top_users_stats = crud.get_users_stats_order_by_tasks(limit=None)
        text = "🧑‍ Рейтинг игроков.\n\n"
        if not top_users_stats:
            return "❗ Рейтинг пуст."
        for user_stats in top_users_stats:
            top_user = crud.get_user(user_stats.user_id)
            text += f"{counter}. {top_user.name} — " \
                    f"{user_stats.personal_tasks} ⭐\n"
            counter += 1
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)
    elif msg[0] == "/club":
        clubs = crud.get_clubs_stats_order_by_tasks(limit=None)
        text = "🏠 Рейтинг клубов.\n\n"
        if not clubs:
            return "❗ Рейтинг пуст."
        for club_stats in clubs:
            club = crud.get_club(club_stats.club_id)
            text += f"{counter}. {club.name} — {club_stats.total_tasks} 🎄\n"
            counter += 1
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/notice user", "/notice club"]))
async def notice_user(event: SimpleBotEvent):
    # Уведомление пользователю
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ", maxsplit=3)
    if msg[1] == "user":
        if crud.get_user(int(msg[2])):
            try:
                await event.api_ctx.messages.send(user_id=int(msg[2]),
                                                  message=msg[3],
                                                  random_id=randint(1,
                                                                    9999999))
            except Exception as e:
                text = f"Не смог отправить сообщение пользователю {msg[2]}\n" \
                       f"Ошибка: {e}"
                notice(text)
            return "✅ Сообщение отправлено."
        else:
            return "❗ Игрок не найден."
    if msg[1] == "club":
        if crud.get_club(int(msg[2])):
            users = crud.get_users_with_club(int(msg[2]))
            for user in users:
                try:
                    await event.api_ctx.messages.send(user_id=user.user_id,
                                                      message=msg[3],
                                                      random_id=randint(1,
                                                                        9999999))
                except Exception as e:
                    text = f"Не смог отправить сообщение пользователю {msg[2]}\n" \
                           f"Ошибка: {e}"
                    notice(text)
            return "✅ Сообщения отправлены."
        else:
            return "❗ Клуб не найден."


@simple_bot_message_handler(admin_router,
                            PayloadFilter({"command": "user_items"}))
async def task_rating(event: SimpleBotEvent):
    items = crud.get_user_items()
    text = "🧸 Предметы игроков.\n\n"
    if not items:
        return "❗ Предметов нет"
    for item in items:
        user = crud.get_user(item.user_id)
        text += f"{item.id}. {user.name} ({user.pet_id}) -- {item.item_name} \n"
    text += "\n +confirm user {id} — подтвердить предмет"
    if len(text) > 4050:
        await event.answer("Сообщение слишком длинное. Для решение "
                           "проблемы напишите разработчику.")
    else:
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            PayloadFilter({"command": "club_items"}))
async def task_rating(event: SimpleBotEvent):
    items = crud.get_club_items()
    text = "🎈 Предметы клубов.\n\n"
    if not items:
        return "❗ Предметов нет"
    for item in items:
        club = crud.get_club(item.club_id)
        text += f"{item.id}. {club.name} ({club.club_id}) -- {item.item_name}\n"
    text += "\n +confirm club {id} — подтвердить предмет"
    if len(text) > 4050:
        await event.answer("Сообщение слишком длинное. Для решение "
                           "проблемы напишите разработчику.")
    else:
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/items user", "/items club"]))
async def items(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[1] == "user":
        items = crud.get_user_items()
        text = "🧸 Предметы игроков.\n\n"
        if not items:
            return "❗ Предметов нет"
        for item in items:
            user = crud.get_user(item.user_id)
            text += f"{item.id}. {user.name} ({user.pet_id}) -- {item.item_name} \n"
        text += "\n +confirm user {id} — подтвердить предмет"
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)
    if msg[1] == "club":
        items = crud.get_club_items()
        text = "🎈 Предметы клубов.\n\n"
        if not items:
            return "❗ Предметов нет"
        for item in items:
            club = crud.get_club(item.club_id)
            text += f"{item.id}. {club.name} ({club.club_id}) -- {item.item_name}\n"
        text += "\n +confirm club {id} — подтвердить предмет"
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter("/club members"))
async def club_members(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    text, counter = "Участники клуба \n", 1
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[2].isdigit() is False:
        return "❗ Клуб не найден."
    club_members = crud.get_users_with_club(msg[2])
    if not club_members:
        return "❗ Клуб не найден."
    for member in club_members:
        user_stats = crud.get_user_stats(member.user_id)
        text += f"{counter}. {member.name} ({member.user_id}) --{user_stats.personal_tasks}\n"
        counter += 1
    if len(text) > 4050:
        await event.answer("Сообщение слишком длинное. Для решение "
                           "проблемы напишите разработчику.")
    else:
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+tasks club members"]))
async def club_members(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[3].isdigit() is False and msg[4].isdigit() is False:
        return "❗ Не смог определить клуб или награду"
    club_members = crud.get_users_with_club(msg[3])
    if not club_members:
        return "❗ Клуб не найден."
    for member in club_members:
        for i in range(int(msg[4])):
            await add_user_points(user_id=member.user_id, point=False)
    return "Награда зачислена"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter("/stats"))
async def stats(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    db = pickledb.load("./stats.db", True)
    total_clicks = db.get("total_clicks")
    amount_users = crud.get_amount_users()
    amount_personal_tasks = crud.get_personal_tasks()
    amount_completed_p_t = crud.get_personal_tasks_with_filter("completed")
    amount_timeout_p_t = crud.get_personal_tasks_with_filter("timeout")
    amount_clubs = crud.get_amount_clubs()
    amount_clubs_tasks = crud.get_clubs_tasks()
    amount_completed_c_t = crud.get_clubs_tasks_with_filter("completed")
    amount_timeout_c_t = crud.get_clubs_tasks_with_filter("timeout")
    users = crud.get_users_stats_order_by_points(limit=None)
    clubs = crud.get_clubs_stats_order_by_points(limit=None)
    amount_1 = 0
    amount_2 = 0
    amount_3 = 0
    amount_4 = 0
    for user in users:
        amount_1 += user.personal_tasks
        amount_2 += user.points
    for club in clubs:
        amount_3 += club.total_tasks
        amount_4 += club.points
    text = f"Статистика для Лерочки 🥰\n" \
           f"👨🏼‍💼 Пользователей: {amount_users}\n" \
           f"📈 Заданий: {amount_personal_tasks}\n" \
           f"✅ Выполнено: {amount_completed_p_t}\n" \
           f"❌ Просрочено: {amount_timeout_p_t}\n\n" \
           f"🎈 Клубов: {amount_clubs}\n" \
           f"📈 Заданий: {amount_clubs_tasks}\n" \
           f"✅ Выполнено: {amount_completed_c_t}\n" \
           f"❌ Просрочено: {amount_timeout_c_t}\n\n" \
           f"⭐️ Всего: {amount_1}\n" \
           f"🏮 Всего: {amount_2}\n" \
           f"🎄 Всего: {amount_3}\n" \
           f"🏵 Всего: {amount_4}\n\n" \
           f"👆🏻 Всего кликов: {total_clicks}"
    return text


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+confirm user"]))
async def club_members(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[2].isdigit() is False:
        if "-" in msg[2]:
            try:
                start, end = msg[2].split("-")
                start = int(start)
                end = int(end)
            except Exception as e:
                return "❗ Не смог определить id наград"
            for item_id in range(start, end + 1):
                crud.confirm_user_item(item_id)
            return "✅ Предметы подтверждены"
        else:
            return "❗ Не смог определить id награды"
    if crud.confirm_user_item(int(msg[2])):
        return "✅ Предмет подтвержден"
    else:
        return "❗ Предмет с таким id не найден"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+confirm club"]))
async def club_members(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[2].isdigit() is False:
        if "-" in msg[2]:
            try:
                start, end = msg[2].split("-")
                start = int(start)
                end = int(end)
            except:
                return "❗ Не смог определить id наград"
            for item_id in range(start, end + 1):
                crud.confirm_club_item(item_id)
            return "✅ Предметы подтверждены"
        else:
            return "❗ Не смог определить id награды"
    if crud.confirm_club_item(int(msg[2])):
        return "✅ Предмет подтвержден"
    else:
        return "❗ Предмет с таким id не найден"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/get user items",
                                                "/get club items"]))
async def club_members(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[3].isdigit() is False:
        return "Укажите количество очков"
    if msg[1] == "user":
        items = crud.get_user_items_with_score(msg[3])
        text = "🧸 Предметы игроков.\n\n"
        if not items:
            return "❗ Предметов нет"
        for item in items:
            user = crud.get_user(item.user_id)
            text += f"{item.id}. {user.name} ({user.pet_id}) -- {item.item_name} \n"
        text += "\n +confirm user {id} — подтвердить предмет"
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)
    if msg[1] == "club":
        items = crud.get_club_items_with_score(msg[3])
        text = "🎈 Предметы клубов.\n\n"
        if not items:
            return "❗ Предметов нет"
        for item in items:
            club = crud.get_club(item.club_id)
            text += f"{item.id}. {club.name} ({club.club_id}) -- {item.item_name}\n"
        text += "\n +confirm club {id} — подтвердить предмет"
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/wipe"]))
async def wipe(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    if crud.wipe():
        return "Рейтинги обнулены."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/ban"]))
async def ban(event: SimpleBotEvent):
    # format /ban {user_id} {hours} {reason}
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ", maxsplit=3)
    if len(msg) < 4:
        return "Пожалуйста, отправьте команду " \
               "в формате:\n/ban {user_id} {hours} {reason}"
    if msg[1].isdigit() is False or msg[2].isdigit() is False:
        return "Будьте внимательны: /ban {user_id} {hours} {reason}"
    user_id = int(msg[1])
    reason = str(msg[3])
    ending = int(msg[2]) * 60 * 60
    ending = int(time.time()) + 10800 + ending
    d = datetime.datetime.utcfromtimestamp(
        ending).strftime('%d')
    m = datetime.datetime.utcfromtimestamp(
        ending).strftime('%m')
    h = datetime.datetime.utcfromtimestamp(
        ending).strftime('%H:%M')
    left_time = f"{d} {month[m]} в {h}"
    if crud.ban(user_id, reason, ending):
        await event.answer(f"Пользователь был забанен.\n"
                           f"Для снятия бана отправьте: /unban {user_id}")
        await event.api_ctx.messages.send(user_id=user_id,
                                          message=f"Вы были забанены.\n"
                                                  f"Причина: {reason}\n"
                                                  f"Окончание бана:"
                                                  f" {left_time}",
                                          random_id=randint(1, 99999999))
    else:
        await event.answer(f"Пользователь уже заблокирован.")


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/unban"]))
async def ban(event: SimpleBotEvent):
    # format /unban {user_id}
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if len(msg) < 2:
        return "Пожалуйста, отправьте команду " \
               "в формате:\n/unban {user_id}"
    if msg[1].isdigit() is False:
        return "Будьте внимательны: /unban {user_id}"
    if crud.unban(int(msg[1])):
        return "Пользователь разблокирован."
    else:
        return "У пользователя нет бана."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/op"]))
async def ban(event: SimpleBotEvent):
    # format /op {user_id} {access}
    current_user = event["current_user"]
    if current_user.access < 3:
        return None
    msg = event.object.object.message.text.split(" ")
    if len(msg) < 3:
        return "Пожалуйста, отправьте команду " \
               "в формате:\n/op {user_id} {access}"
    if msg[1].isdigit() is False or msg[2].isdigit() is False:
        return "Будьте внимательны: /op {user_id} {access}"
    user_id = int(msg[1])
    access = int(msg[2])
    if access < 0 or access > 3:
        return "Такой должности не существует"
    crud.update_user_access(user_id=user_id, access=access)
    await event.api_ctx.messages.send(user_id=user_id,
                                      message=f"Вас повысили "
                                              f"до должости "
                                              f"{access_name[access]}",
                                      random_id=randint(1, 99999999))
    return f"Пользователь повышен до должности {access_name[access]}."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/unop"]))
async def ban(event: SimpleBotEvent):
    # format //unop {user_id} {access}
    current_user = event["current_user"]
    if current_user.access < 3:
        return None
    msg = event.object.object.message.text.split(" ")
    if len(msg) < 3:
        return "Пожалуйста, отправьте команду " \
               "в формате:\n/unop {user_id} {access}"
    if msg[1].isdigit() is False or msg[2].isdigit() is False:
        return "Будьте внимательны: /unop {user_id} {access}"
    user_id = int(msg[1])
    access = int(msg[2])
    if access < 0 or access > 3:
        return "Такой должности не существует"
    crud.update_user_access(user_id=user_id, access=access)
    await event.api_ctx.messages.send(user_id=user_id,
                                      message=f"Вас понизили "
                                              f"до должости "
                                              f"{access_name[access]}.",
                                      random_id=randint(1, 99999999))
    return f"Пользователь понижен до должности {access_name[access]}"

