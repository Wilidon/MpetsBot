import datetime
import time
from random import randint

import pickledb
from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter, MessageArgsFilter, TextContainsFilter,
)

from config import get_db
from sql import crud
from utils import functions
from utils.collection_handler import add_collection_item, remove_collection_item
from utils.functions import add_user_points, add_club_points, notice
from utils.constants import month, access_name, prizes, c_prizes, collections, numbers, bosses

admin_router = DefaultRouter()


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["+points user", "+points club",
                                 "-points user", "-points club"]),
                            MessageArgsFilter(args_count=2, command_length=2))
async def points(event: SimpleBotEvent):
    # format +points user {user_id} {points}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
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
async def personal_tasks(event: SimpleBotEvent):
    # format +tasks user {user_id} {points}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split()
    if msg[1] == "user":
        if msg[0] == "+tasks":
            if crud.get_user(int(msg[2])):
                for i in range(int(msg[3])):
                    await add_user_points(user_id=int(msg[2]), point=False)
                return "✅ 🌼 начислены."
            else:
                return "❗ Игрок не найден."
        elif msg[0] == "-tasks":
            if crud.get_user(int(msg[2])):
                crud.update_user_stats(int(msg[2]), personal_tasks=-int(msg[
                                                                            3]))
                return "✅ 🌼 списаны."
            else:
                return "❗ Игрок не найден."
    if msg[1] == "club":
        if msg[0] == "+tasks":
            if crud.get_club(int(msg[2])):
                for i in range(int(msg[3])):
                    await add_club_points(club_id=int(msg[2]), point=False)
                return "✅ 🦋 начислены."
            else:
                return "❗ Клуб не найден."
        elif msg[0] == "-tasks":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), total_tasks=-int(msg[3]))
                return "✅ 🦋 списаны."
            else:
                return "❗ Клуб не найден."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/user rating", "/club rating"]))
async def user_rating(event: SimpleBotEvent):
    # format /user rating
    current_user, counter = event["current_user"], 1
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split()
    if msg[0] == "/user":
        top_users_stats = crud.get_users_stats_order_by_points(limit=100)
        text = "🧑‍ Рейтинг игроков.\n\n"
        if not top_users_stats:
            return "❗ Рейтинг пуст."
        for user_stats in top_users_stats:
            top_user = crud.get_user(user_stats.user_id)
            text += f"{counter}. [id{top_user.user_id}|{top_user.name}] " \
                    f"({top_user.pet_id}) — {user_stats.points} 🏅\n"
            counter += 1
        if len(text) > 4050:
            await event.answer("Сообщение слишком длинное. Для решение "
                               "проблемы напишите разработчику.")
        else:
            await event.answer(text)
    elif msg[0] == "/club":
        clubs = crud.get_clubs_stats_order_by_points(limit=100)
        text = "🏠 Рейтинг клубов.\n\n"
        if not clubs:
            return "❗ Рейтинг пуст."
        for club_stats in clubs:
            club = crud.get_club(club_stats.club_id)
            text += f"{counter}. {club.name} ({club.club_id}) —" \
                    f" {club_stats.points} 🎈\n"
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
    top_users_stats = crud.get_users_stats_order_by_tasks(limit=1000)
    text = "🧑‍ Рейтинг игроков.\n\n"
    if not top_users_stats:
        return "❗ Рейтинг пуст."
    for user_stats in top_users_stats:
        top_user = crud.get_user(user_stats.user_id)
        text += f"{counter}. {top_user.name} — " \
                f"{user_stats.personal_tasks} 🌼/" \
                f"{user_stats.points}🏅\n"
        counter += 1
        if len(text) > 4050:
            await event.answer(text)
            text = "🧑‍ Рейтинг игроков.\n\n"
    await event.answer(text)


@simple_bot_message_handler(admin_router,
                            PayloadFilter({"command": "rating_club_tasks"}))
async def task_rating(event: SimpleBotEvent):
    current_user, counter = event["current_user"], 1
    clubs = crud.get_clubs_stats_order_by_tasks(limit=1000)
    text = "🏠 Рейтинг клубов.\n\n"
    if not clubs:
        return "❗ Рейтинг пуст."
    for club_stats in clubs:
        club = crud.get_club(club_stats.club_id)
        text += f"{counter}. {club.name} — {club_stats.total_tasks} 🦋/" \
                f"{club_stats.points}🎈\n"
        counter += 1
        if len(text) > 4050:
            await event.answer(text)
            text = "🏠 Рейтинг клубов.\n\n"
    await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/notice user", "/notice club"]))
async def notice_user(event: SimpleBotEvent):
    # format /notice user {user_id} {message}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
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
        text += f"{item.id}. {user.pet_id} ({user.user_id}) — {user.name} — {item.item_name} \n"
        if len(text) > 3950:
            await event.answer(text)
            text = "🧸 Предметы игроков.\n\n"
    text += "\n +confirm user {id} — подтвердить предмет"
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
        text += f"{item.id}. {club.club_id} — {club.name} — {item.item_name}\n"
        if len(text) > 3950:
            await event.answer(text)
            text = "🎈 Предметы клубов.\n\n"
    text += "\n +confirm club {id} — подтвердить предмет"
    await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter("/club members"))
async def club_member(event: SimpleBotEvent):
    # format /club members {club_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    text, counter = "Участники клуба \n", 1
    msg = event.object.object.message.text.split(" ")
    if msg[2].isdigit() is False:
        return "❗ Клуб не найден."
    club_id = int(msg[2])
    club_members = crud.get_users_with_club(club_id)
    if not club_members:
        return "❗ Клуб не найден."
    for member in club_members:
        user_stats = crud.get_user_stats(member.user_id)
        text += f"{counter}. {member.name} ({member.pet_id}) --" \
                f"{user_stats.personal_tasks}🦋/{user_stats.points}🎈\n"
        counter += 1
    if len(text) > 4050:
        await event.answer("Сообщение слишком длинное. Для решение "
                           "проблемы напишите разработчику.")
    else:
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+tasks club members"]))
async def club_member(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if msg[3].isdigit() is False and msg[4].isdigit() is False:
        return "❗ Не смог определить клуб или награду"
    club_id = int(msg[3])
    club_members = crud.get_users_with_club(club_id)
    if not club_members:
        return "❗ Клуб не найден."
    for member in club_members:
        for i in range(int(msg[4])):
            await add_user_points(user_id=member.user_id, point=False)
    return "Награда зачислена"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+confirm user"]))
async def confirm_user(event: SimpleBotEvent):
    # format +confirm user {item_id} [{item_id}-{item_id}]
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
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
async def confirm_club(event: SimpleBotEvent):
    # format +confirm club {item_id} [{item_id}-{item_id}]
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
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
                crud.confirm_club_item(item_id)
            return "✅ Предметы подтверждены"
        else:
            return "❗ Не смог определить id награды"
    if crud.confirm_club_item(int(msg[2])):
        return "✅ Предмет подтвержден"
    else:
        return "❗ Предмет с таким id не найден"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/wipe"]))
async def wipe(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    if crud.wipe():
        return "Рейтинги обнулены."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/totalwipe"]))
async def wipe(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    if crud.total_wipe():
        return "Рейтинги обнулены."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/megatotalwipe"]))
async def wipe(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    if crud.mega_total_wipe():
        return "Рейтинги обнулены."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/ban"]))
async def ban(event: SimpleBotEvent):
    # format /ban {user_id} {hours} {reason}
    current_user = event["current_user"]
    if current_user.access <= 1:
        return False
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
        return False
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
        return False
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
                                              f"до должности "
                                              f"{access_name[access]}",
                                      random_id=randint(1, 99999999))
    return f"Пользователь повышен до должности {access_name[access]}."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/unop"]))
async def ban(event: SimpleBotEvent):
    # format /unop {user_id} {access}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
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


@simple_bot_message_handler(admin_router,
                            TextContainsFilter("/stats"))
async def stats(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access < 2:
        return False
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
           f"🌼️ Всего: {amount_1}\n" \
           f"🏅 Всего: {amount_2}\n" \
           f"🦋 Всего: {amount_3}\n" \
           f"🎈 Всего: {amount_4}\n\n" \
           f"👆🏻 Всего кликов: {total_clicks}"
    return text


@simple_bot_message_handler(admin_router,
                            TextContainsFilter("/stagestats"))
async def totalstats(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access < 2:
        return False
    stage_0 = stage_1 = stage_2 = stage_3 = stage_4 = stage_5 = stage_6 = stage_7 = stage_8 = 0
    c_stage_0 = c_stage_1 = c_stage_2 = c_stage_3 = c_stage_4 = c_stage_5 = c_stage_6 = c_stage_7 = 0
    c_stage_8 = c_stage_9 = c_stage_10 = c_stage_11 = 0
    item_1 = item_2 = item_3 = item_4 = item_5 = item_6 = item_7 = item_8 = 0
    c_item_1 = c_item_2 = c_item_3 = c_item_4 = c_item_5 = c_item_6 = c_item_7 = c_item_8 = c_item_9 = c_item_10 = 0
    c_item_11 = 0
    users = crud.get_users_stats_order_by_points(limit=9999)
    for user in users:
        if 0 <= user.personal_tasks < 10:
            stage_0 += 1
        elif 10 <= user.personal_tasks < 25:
            stage_1 += 1
        elif 25 <= user.personal_tasks < 40:
            stage_2 += 1
        elif 40 <= user.personal_tasks < 70:
            stage_3 += 1
        elif 70 <= user.personal_tasks < 100:
            stage_4 += 1
        elif 100 <= user.personal_tasks < 125:
            stage_5 += 1
        elif 125 <= user.personal_tasks < 160:
            stage_6 += 1
        elif 160 <= user.personal_tasks < 177:
            stage_7 += 1
        elif 177 <= user.personal_tasks:
            stage_8 += 1
    clubs = crud.get_clubs_stats_order_by_points(limit=9999)
    for club in clubs:
        if 0 <= club.total_tasks < 30:
            c_stage_0 += 1
        elif 30 <= club.total_tasks < 70:
            c_stage_1 += 1
        elif 70 <= club.total_tasks < 160:
            c_stage_2 += 1
        elif 160 <= club.total_tasks < 230:
            c_stage_3 += 1
        elif 230 <= club.total_tasks < 350:
            c_stage_4 += 1
        elif 350 <= club.total_tasks < 510:
            c_stage_5 += 1
        elif 510 <= club.total_tasks < 620:
            c_stage_6 += 1
        elif 620 <= club.total_tasks < 800:
            c_stage_7 += 1
        elif 800 <= club.total_tasks < 980:
            c_stage_8 += 1
        elif 980 <= club.total_tasks < 1111:
            c_stage_9 += 1
        elif 1111 <= club.total_tasks < 1239:
            c_stage_10 += 1
        elif 1239 <= club.total_tasks:
            c_stage_11 += 1
    user_items = crud.get_all_user_items()
    for item in user_items:
        if item.score == 10:
            item_1 += 1
        elif item.score == 25:
            item_2 += 1
        elif item.score == 40:
            item_3 += 1
        elif item.score == 70:
            item_4 += 1
        elif item.score == 100:
            item_5 += 1
        elif item.score == 125:
            item_6 += 1
        elif item.score == 160:
            item_7 += 1
        elif item.score == 177:
            item_8 += 1
    club_items = crud.get_all_club_items()
    for item in club_items:
        if item.score == 30:
            c_item_1 += 1
        elif item.score == 70:
            c_item_2 += 1
        elif item.score == 160:
            c_item_3 += 1
        elif item.score == 230:
            c_item_4 += 1
        elif item.score == 350:
            c_item_5 += 1
        elif item.score == 510:
            c_item_6 += 1
        elif item.score == 620:
            c_item_7 += 1
        elif item.score == 800:
            c_item_8 += 1
        elif item.score == 980:
            c_item_9 += 1
        elif item.score == 1111:
            c_item_10 += 1
        elif item.score == 1239:
            c_item_11 += 1
    text = f"Статистика для Лерочки 🥰\n" \
           f"👨🏼‍💼 На 0 этапе: {stage_0}\n" \
           f"👨🏼‍💼 На 1 этапе: {stage_1}\n" \
           f"👨🏼‍💼 На 2 этапе: {stage_2}\n" \
           f"👨🏼‍💼 На 3 этапе: {stage_3}\n" \
           f"👨🏼‍💼 На 4 этапе: {stage_4}\n" \
           f"👨🏼‍💼 На 5 этапе: {stage_5}\n" \
           f"👨🏼‍💼 На 6 этапе: {stage_6}\n" \
           f"👨🏼‍💼 На 7 этапе: {stage_7}\n" \
           f"👨🏼‍💼 Прошли гонку: {stage_8}\n\n" \
           f"🎈 На 0 этапе: {c_stage_0}\n" \
           f"🎈 На 1 этапе: {c_stage_1}\n" \
           f"🎈 На 2 этапе: {c_stage_2}\n" \
           f"🎈 На 3 этапе: {c_stage_3}\n" \
           f"🎈 На 4 этапе: {c_stage_4}\n" \
           f"🎈 На 5 этапе: {c_stage_5}\n" \
           f"🎈 На 6 этапе: {c_stage_6}\n" \
           f"🎈 На 7 этапе: {c_stage_7}\n" \
           f"🎈 На 8 этапе: {c_stage_8}\n" \
           f"🎈 На 9 этапе: {c_stage_9}\n" \
           f"🎈 На 10 этапе: {c_stage_10}\n" \
           f"🎈 Прошли гонку: {c_stage_11}\n\n" \
           f"{prizes[10]}: {item_1}\n" \
           f"{prizes[25]}: {item_2}\n" \
           f"{prizes[40]}: {item_3}\n" \
           f"{prizes[70]}: {item_4}\n" \
           f"{prizes[100]}: {item_5}\n" \
           f"{prizes[125]}: {item_6}\n" \
           f"{prizes[160]}: {item_7}\n" \
           f"{prizes[177]}: {item_8}\n\n" \
           f"{c_prizes[30]}: {c_item_1}\n" \
           f"{c_prizes[70]}: {c_item_2}\n" \
           f"{c_prizes[160]}: {c_item_3}\n" \
           f"{c_prizes[230]}: {c_item_4}\n" \
           f"{c_prizes[350]}: {c_item_5}\n" \
           f"{c_prizes[510]}: {c_item_6}\n" \
           f"{c_prizes[620]}: {c_item_7}\n" \
           f"{c_prizes[800]}: {c_item_8}\n" \
           f"{c_prizes[980]}: {c_item_9}\n" \
           f"{c_prizes[1111]}: {c_item_10}\n" \
           f"{c_prizes[1239]}: {c_item_11}"
    await event.answer(message=text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/pt"]))
async def personal_task_handler(event: SimpleBotEvent):
    # format /pt {user_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if msg[1].isdigit() is False:
        return "Будьте внимательны: /pt {user_id}"
    user_id = int(msg[1])
    today = int(datetime.datetime.today().strftime("%Y%m%d"))
    tasks = crud.get_user_tasks(user_id, today)
    text = "Задания\n"
    for task in tasks:
        text += f"{task.id}. {task.task_name} - {task.progress}/{task.end}\n"
    return text


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/ct"]))
async def club_task_handler(event: SimpleBotEvent):
    # format /ut {user_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if msg[1].isdigit() is False:
        return "Будьте внимательны: /ut {user_id}"
    user_id = int(msg[1])
    today = int(datetime.datetime.today().strftime("%Y%m%d"))
    tasks = crud.get_club_tasks_without_status(user_id, today)
    text = "Задания\n"
    for task in tasks:
        text += f"{task.id}. {task.task_name} - {task.progress}/{task.end}\n"
    return text


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/cut"]))
async def completed_user_task_handler(event: SimpleBotEvent):
    # format /cut {id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if msg[1].isdigit() is False:
        return "Будьте внимательны: /cut {id}"
    task_id = int(msg[1])
    task = crud.get_user_task(id=task_id)
    crud.update_user_task(id=task_id, progress=task.end, status="completed")
    await functions.add_user_points(user_id=task.user_id,
                                    task_name=task.task_name)
    return "Задание подтверждено"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/cct"]))
async def completed_club_task_handler(event: SimpleBotEvent):
    # format /cct {id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if msg[1].isdigit() is False:
        return "Будьте внимательны: /cct {id}"
    task_id = int(msg[1])
    task = crud.get_club_task(id=task_id)
    club_id = crud.get_user(task.user_id).club_id
    crud.update_club_task(id=task_id, progress=task.end, status="completed")
    await functions.add_club_points(user_id=task.user_id,
                                    club_id=club_id,
                                    task_name=task.task_name)
    return "Задание подтверждено"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/usertasks"]))
async def user_tasks_handler(event: SimpleBotEvent):
    # format /usertask
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    db = get_db()
    resp = db.lgetall("user_tasks")
    return str(resp)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/add usertask"]))
async def add_user_tasks_handler(event: SimpleBotEvent):
    # format /add usertask {task_name}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    task_name = msg[2]
    db = get_db()
    db.ladd("user_tasks", task_name)
    return "Задание добавлено"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/del usertask"]))
async def deleteuser_tasks_handler(event: SimpleBotEvent):
    # format /del usertask {task_name}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    task_name = msg[2]
    db = get_db()
    if db.lexists("user_tasks", task_name) is True:
        r = db.lgetall("user_tasks")
        for i in range(len(r)):
            if r[i] == task_name:
                db.lpop("user_tasks", i)
                break
    return "Задание удалено"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/clubtasks"]))
async def club_tasks_handler(event: SimpleBotEvent):
    # format /clubtask
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    db = get_db()
    resp = db.lgetall("club_tasks")
    return str(resp)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/add clubtask"]))
async def add_club_tasks_handler(event: SimpleBotEvent):
    # format /add clubtask {task_name}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    task_name = msg[2]
    db = get_db()
    db.ladd("club_tasks", task_name)
    return "Задание добавлено"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/del clubtask"]))
async def del_club_tasks_handler(event: SimpleBotEvent):
    # format /del clubtask {task_name}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    task_name = msg[2]
    db = get_db()
    if db.lexists("club_tasks", task_name) is True:
        r = db.lgetall("club_tasks")
        for i in range(len(r)):
            if r[i] == task_name:
                db.lpop("club_tasks", i)
                break
    return "Задание удалено"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+collection"]))
async def del_club_tasks_handler(event: SimpleBotEvent):
    # format +collection {user_id} {collection_id} {part_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 4:
        return "format +collection {user_id} {collection_id} {part_id}"
    user_id = int(msg[1])
    part_id = int(msg[3])
    collection_id = int(msg[2])
    await add_collection_item(user_id=user_id,
                              collection_id=collection_id,
                              part_id=part_id)
    return "Часть коллекции начислена."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["-collection"]))
async def del_club_tasks_handler(event: SimpleBotEvent):
    # format -collection {user_id} {collection_id} {part_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 4:
        return "format -collection {user_id} {collection_id} {part_id}"
    user_id = int(msg[1])
    part_id = int(msg[3])
    collection_id = int(msg[2])
    await remove_collection_item(user_id=user_id,
                                 collection_id=collection_id,
                                 part_id=part_id)
    return "Часть коллекции снята."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/collection"]))
async def collection_list(event: SimpleBotEvent):
    # format /collection {user_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 2:
        return "format /collection {user_id}"
    user_id = int(msg[1])
    text = "🧩Коллекции\n\n"
    counter = 0
    for collection in collections.items():
        collection_id = collection[0]
        user_collection = crud.get_user_collection(user_id=user_id,
                                                   collection_id=collection_id)
        colletion_name = collection[1]['name']
        required = collection[1]['required']
        reward = collection[1]['reward']
        text += f"{numbers[counter + 1]} {colletion_name} \n" \
                f"Необходимо: \n"
        for data in required:
            text += f"{data['icon']} (х{data['amount']}) "
        text += f"\nСобрано: "
        counter_types = 1
        for data in required:
            amount = user_collection.__dict__['type' + str(counter_types)]
            text += f"{data['icon']} (х{amount}) "
            counter_types += 1
        text += f"\nНаграда за коллекцию: {reward}\n\n"
        counter += 1
    return text


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/bosses"]))
async def add_club_tasks_handler(event: SimpleBotEvent):
    # format /bosses
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    text = "Боссы\n\n"
    for boss_id, boss in bosses.items():
        text += f"{boss_id} | {boss.get('name')} | {boss.get('health_points')}❤\n" \
                f"Баффы:\n" \
                f"Аватар: {boss.get('avatar_name')}\n" \
                f"Статус: {boss.get('about')}\n" \
                f"\n" \
                f"Награды:\n" \
                f"За убийство: {boss.get('reward_killed')}\n" \
                f"Топ 1 по урону: {boss.get('top1user')}\n" \
                f"Топ 2 по урону: {boss.get('top2user')}\n" \
                f"Топ 3 по урону: {boss.get('top3user')}\n" \
                f"Каждые 500 урона: {boss.get('every500damage')}\n" \
                f"\n" \
                f"Топ 1 по урону: {boss.get('top1club')}\n" \
                f"Топ 2 по урону: {boss.get('top2club')}\n" \
                f"Топ 3 по урону: {boss.get('top3club')}\n" \
                f"Каждые 3000 урона: {boss.get('every3000damage')}\n\n"
    return text


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/boss"]))
async def add_club_tasks_handler(event: SimpleBotEvent):
    # format /boss {start_date} {end_date}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 3:
        return "format /boss {start_date} {end_date}"
    boss_start = int(msg[1])
    boss_end = int(msg[2])
    db = get_db()
    db.set("boss_start", boss_start)
    db.set("boss_end", boss_end)
    return "Даты установлены."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+boss"]))
async def del_club_tasks_handler(event: SimpleBotEvent):
    # format +boss {boss_id} {health_points}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 3:
        return "format +boss {boss_id} {health_points}"
    boss_id = int(msg[1])
    health_points = int(msg[2])
    crud.restart_user_time()
    crud.create_boss(boss_id=boss_id,
                     health_points=health_points)
    return "Босс создан."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/rewards"]))
async def add_club_tasks_handler(event: SimpleBotEvent):
    # format /rewards {boss_id}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 2:
        return "format /rewards {boss_id}"
    boss_id = int(msg[1])
    text = "Награды за босса\n\n"
    user_rewards = crud.get_users_boss_reward(boss_id=boss_id)
    for i in range(len(user_rewards)):
        user = user_rewards[i]
        current_user = crud.get_user(user_id=user.user_id)
        if 0 <= i <= 2:
            text += f"{i+1}. {current_user.name} [{current_user.user_id}] ({current_user.pet_id}) - " \
                    f"{user.reward} [{user.total_damage}]\n"
        else:
            text += f"{i + 1}. {current_user.name} [{current_user.user_id}] - " \
                    f"{user.reward} [{user.total_damage}]\n"
        if len(text) > 3950:
            await event.answer(text)
            text = "Награды за босса\n\n"
    await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["+hp"]))
async def add_club_tasks_handler(event: SimpleBotEvent):
    # format +hp {health}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 2:
        return "format +hp {health}"
    hp = int(msg[1])
    boss = crud.get_current_boss()
    crud.update_boss_health(boss_id=boss.id, damage=-hp)
    return f"Вы добавили {hp} здоровья"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["-hp"]))
async def add_club_tasks_handler(event: SimpleBotEvent):
    # format -hp {health}
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) != 2:
        return "format -hp {health}"
    hp = int(msg[1])
    boss = crud.get_current_boss()
    crud.update_boss_health(boss_id=boss.id, damage=hp)
    return f"Вы сняли {hp} здоровья"


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/bstats"]))
async def help(event: SimpleBotEvent):
    # format /bstats
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    msg = event.object.object.message.text.split(" ")
    if len(msg) == 1:
        boss_id = crud.get_current_boss()
        boss_id = boss_id.id
    else:
        boss_id = int(msg[1])
    text = "Статистика босса\n"
    s = crud.get_boss_stats(boss_id=boss_id)
    d, t, total_damage = {}, 0, 0
    for i in s:
        now = i.damage_time
        timestamp = int(datetime.datetime.timestamp(now))
        if t == 0:
            t = timestamp + 43200
            t_old = timestamp
        if t < timestamp:
            t = timestamp + 43200
            t_old = timestamp
        if d.get(t_old) is None:
            d[t_old] = i.damage
        else:
            d[t_old] += i.damage
    for g, h in d.items():
        total_damage += h
        start = datetime.datetime.fromtimestamp(g + 10800)
        end = datetime.datetime.fromtimestamp(g + 10800 + 43200)
        text += f"{start} - {end} | {h}\n"
    text += f"\nВсего урона: {total_damage}"
    await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/health"]))
async def help(event: SimpleBotEvent):
    # format /health
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    health = crud.health()
    text = f"🟢 Состояние бота\n" \
           f"♻️ Обход пользователей: {health.userinfo}с\n" \
           f"📃 Личные задания: {health.usertasks}с\n" \
           f"🧾 Клубные задания: {health.clubtasks}с\n" \
           f"❄️ Снежки: {health.charm}с\n" \
           f"🐴 Скачки: {health.races}с\n" \
           f"\n" \
           f"🩸 Здоровье бота: {randint(0, 100)}❤"
    await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(["/help"]))
async def help(event: SimpleBotEvent):
    # format /help
    current_user = event["current_user"]
    if current_user.access < 3:
        return False
    text = "Помощь\n" \
           "+points club {club_id} {points} — добавить фишки (рейтинг);\n" \
           "+tasks club {club_id} {points} — добавить елки (гонка);\n" \
           "+points user {user_id} {points} — добавить баллы (рейтинг);\n" \
           "+tasks user {user_id} {points} — добавить звездочки (гонка);\n" \
           "\n" \
           "/user tasks — первые 100 пользователей рейтинга;\n" \
           "/user club — первые 100 клубов рейтинга;\n" \
           "\n" \
           "/notice user {user_id} {message} — отправить сообщение игроку;\n" \
           "/notice club {club_id} {message} — отправить всему клубу " \
           "сообщение;\n" \
           "\n" \
           "/club members {club_id} — посмотреть список участников клуба;\n" \
           "+tasks club members {club_id} {points} — начислить всем " \
           "участникам клуба звездочки;\n" \
           "\n" \
           "/ban {user_id} {hours} {reason} — забанить пользователя;\n" \
           "/unban {user_id} {hours} {reason} — разбанить пользователя;\n" \
           "\n" \
           "/op {user_id} {access} — повысить пользователя;\n" \
           "/unop {user_id} {access} — понизить пользователя;\n" \
           "\n" \
           "/stats — статистика;\n" \
           "/stagestats — статистика по гонке и призам;\n" \
           "/taskstats — статистика по заданиям ( в будущем );\n" \
           "\n" \
           "+collection {user_id} {collection_id} {part_id};\n" \
           "\n" \
           "/boss {start_date} {end_date} — даты проведения мероприятия [319 325];\n" \
           "+boss {boss_id} {health_points} — создать босса;\n" \
           "/bosses — список боссов (только смысл?);" \
           ""
    await event.answer(text)
