import datetime
from random import randint

from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter, MessageArgsFilter, CommandsFilter, TextContainsFilter,
)
from sql import crud
from utils.constants import SHOP_1, SHOP_2, SHOP_3
from utils.functions import add_user_points, add_club_points

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
                return "Баллы начислены."
            else:
                return "Игрок не найден."
        elif msg[0] == "-points":
            if crud.get_user(int(msg[2])):
                crud.update_user_stats(int(msg[2]), points=-int(msg[3]))
                return "Баллы списаны."
            else:
                return "Игрок не найден."
    if msg[1] == "club":
        if msg[0] == "+points":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), points=int(msg[3]))
                return "Баллы начислены."
            else:
                return "Игрок не найден."
        elif msg[0] == "-points":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), points=-int(msg[3]))
                return "Баллы списаны."
            else:
                return "Игрок не найден."


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
                return "Звездочки начислены."
            else:
                return "Игрок не найден."
        elif msg[0] == "-tasks":
            if crud.get_user(int(msg[2])):
                crud.update_user_stats(int(msg[2]), personal_tasks=-int(msg[
                                                                            3]))
                return "Звездочки списаны."
            else:
                return "Игрок не найден."
    if msg[1] == "club":
        if msg[0] == "+tasks":
            if crud.get_club(int(msg[2])):
                for i in range(int(msg[3])):
                    await add_club_points(club_id=int(msg[2]), point=False)
                return "Ёлки начислены."
            else:
                return "Клуб не найден."
        elif msg[0] == "-tasks":
            if crud.get_club(int(msg[2])):
                crud.update_club_stats(int(msg[2]), total_tasks=-int(msg[3]))
                return "Ёлки списаны."
            else:
                return "Клуб не найден."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/user rating", "/club rating"]))
async def points_rating(event: SimpleBotEvent):
    # Рейтинг пользователей
    current_user, counter = event["current_user"], 1
    msg = event.object.object.message.text.split()
    if msg[0] == "+user":
        top_users_stats = crud.get_users_stats(limit=None)
        text = "🧑‍ Рейтинг игроков.\n"
        if not top_users_stats:
            return "Рейтинг пуст."
        for user_stats in top_users_stats:
            top_user = crud.get_user(user_stats.user_id)
            text += f"{counter}. {top_user.name} — {user_stats.points} 🏮\n"
            counter += 1
        await event.answer(text)
    elif msg[0] == "+club":
        clubs = crud.get_clubs_stats(limit=None)
        text = "🏠 Рейтинг клубов.\n"
        if not clubs:
            return "Рейтинг пуст."
        for club_stats in clubs:
            club = crud.get_club(club_stats.club_id)
            text += f"{counter}. {club.name} — {club_stats.points} 🏵\n"
            counter += 1
        await event.answer(text)


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/user tasks", "/club tasks"]))
async def task_rating(event: SimpleBotEvent):
    # Рейтинг пользователей
    current_user, counter = event["current_user"], 1
    msg = event.object.object.message.text.split()
    if msg[0] == "+user":
        top_users_stats = crud.get_users_stats(limit=None)
        text = "🧑‍ Рейтинг игроков.\n"
        if not top_users_stats:
            return "Рейтинг пуст."
        for user_stats in top_users_stats:
            top_user = crud.get_user(user_stats.user_id)
            text += f"{counter}. {top_user.name} — " \
                    f"{user_stats.personal_tasks} ⭐\n"
            counter += 1
        await event.answer(text)
    elif msg[0] == "+club":
        clubs = crud.get_clubs_stats(limit=None)
        text = "🏠 Рейтинг клубов.\n"
        if not clubs:
            return "Рейтинг пуст."
        for club_stats in clubs:
            club = crud.get_club(club_stats.club_id)
            text += f"{counter}. {club.name} — {club_stats.total_tasks} 🎄\n"
            counter += 1
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
            await event.api_ctx.messages.send(user_id=int(msg[2]),
                                              message=msg[3],
                                              random_id=randint(1, 9999999))
            return "Сообщение отправлено."
        else:
            return "Игрок не найден."
    if msg[1] == "club":
        if crud.get_club(int(msg[2])):
            users = crud.get_users_with_club(int(msg[2]))
            for user in users:
                await event.api_ctx.messages.send(user_id=int(user.user_id),
                                                  message=msg[3],
                                                  random_id=randint(1,
                                                                    9999999))
            return "Сообщения отправлены."
        else:
            return "Клуб не найден."


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["/items user", "/items club"]))
async def items(event: SimpleBotEvent):
    current_user = event["current_user"]
    if current_user.access <= 1:
        return None
    msg = event.object.object.message.text.split(" ")
    if msg[1] == "user":
        counter = 1
        items = crud.get_user_items()
        text = "🧸 Предметы игроков.\n"
        if not items:
            return "Предметов нет"
        for item in items:
            user = crud.get_user(item.user_id)
            text += f"{counter}. {item.item_name} -- {user.name}"
            counter +=1
        return text
    if msg[1] == "club":
        counter = 1
        items = crud.get_club_items()
        text = "🎈 Предметы клубов.\n"
        if not items:
            return "Предметов нет"
        for item in items:
            club = crud.get_club(item.club_id)
            text += f"{counter}. {item.item_name} -- {club.name}"
            counter += 1
        return text


'''@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["shop1"]))
async def points(event: SimpleBotEvent):
    await event.answer(message="shop1",
                       keyboard=SHOP_1.get_keyboard())


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["shop2"]))
async def points(event: SimpleBotEvent):
    await event.answer(message="shop2",
                       keyboard=SHOP_2.get_keyboard())


@simple_bot_message_handler(admin_router,
                            TextContainsFilter(
                                ["shop3"]))
async def points(event: SimpleBotEvent):
    await event.answer(message="shop3",
                       keyboard=SHOP_3.get_keyboard())'''