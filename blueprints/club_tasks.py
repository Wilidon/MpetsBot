from datetime import datetime

from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter, TextContainsFilter,
)
from loguru import logger
from mpetsapi import MpetsApi
from sql import crud
from utils.functions import get_limits, club_tasks_list, club_completed_tasks_list, \
    gifts_name
from utils.tasks import checking_sendGift_task

club_router = DefaultRouter()


@simple_bot_message_handler(club_router,
                            PayloadFilter({"command": "club_tasks"}))
async def profile(event: SimpleBotEvent):
    # Список заданий игрока для клуба
    current_user = event["current_user"]
    if current_user.club_id == 0:
        return "Вы не состоите в клубе."
    current_user_club = crud.get_club(current_user.club_id)
    if current_user_club is None:
        mpets = MpetsApi()
        account = await mpets.start()
        pet = await mpets.view_profile(current_user.pet_id)
        club = await mpets.club(current_user.club_id)
        if account["status"] != "ok" \
                and pet["status"] != "ok" and club["status"] != "ok":
            log = logger.bind(context=f"account {account}")
            log.warning(f"Ошибка при создании клуба. Пользователь:"
                        f" {current_user.user_id}")
            logger.bind(context=f"pet {pet}").warning("Ошибка при создании клуба")
            logger.bind(context=f"club {club}").warning("Ошибка при создании клуба")
            return "❗ Ошибка, пожалуйста, попробуйте ещё раз."
        elif pet["rank"] in ['Куратор', 'Зам. Директора', 'Директор']:
            await event.answer("Ваш клуб не зарегистрирован в системе. "
                               "Через несколько секунд в клуб будет "
                               "отправлена заявка.")
            crud.create_club(current_user.club_id, club["club_name"],
                             account["pet_id"], account["name"],
                             account["password"])
            await mpets.enter_club(current_user.club_id)
            return f"Игрок {account['name']} отправил заявку в клуб. Примите " \
                   f"его и задания активируются. "
        else:
            return "Ваш клуб не зарегистрирован в системе. Попросите игрока, " \
                   "который имеет должность куратора или выше, " \
                   "зарегистрировать клуб в системе. "
    elif current_user_club.status == "waiting":
        await event.answer(f"Ожидаем принятия игрока "
                           f"{current_user_club.bot_name} в клуб.")
        mpets = MpetsApi(current_user_club.bot_name,
                         current_user_club.bot_password)
        await mpets.login()
        await mpets.enter_club(current_user_club.club_id)
    elif current_user_club.status == "excluded":
        mpets = MpetsApi(current_user_club.bot_name,
                         current_user_club.bot_password)
        account = await mpets.login()
        pet = await mpets.view_profile(current_user.pet_id)
        club = await mpets.club(current_user.club_id)
        if account["status"] != "ok" \
                and pet["status"] != "ok" and club["status"] != "ok":
            log = logger.bind(context=f"account {account}")
            log.warning(f"Ошибка при отправке запроса. Пользователь:"
                        f" {current_user.user_id}")
            logger.bind(context=f"pet {pet}").warning("Ошибка при создании клуба")
            logger.bind(context=f"club {club}").warning("Ошибка при создании клуба")
            return "❗ Ошибка, пожалуйста, попробуйте ещё раз."
        if pet["rank"] in ['Куратор', 'Зам. Директора', 'Директор']:
            await event.answer(f"Игрок {current_user_club.bot_name} был исключен из вашего "
                               f"клуба. Примите его обратно и задания "
                               f"активируются.")
            crud.update_club_status(current_user_club.club_id, "waiting")
            await mpets.enter_club(current_user.club_id)
        else:
            return f"Игрок {current_user_club.bot_name} был исключён из " \
                   f"клуба. Попросите " \
                   f"игрока, который имеет должность куратора или выше, " \
                   f"зарегистрировать клуб в системе. "
    else:
        today = int(datetime.today().strftime("%Y%m%d"))
        tasks = crud.get_club_tasks(current_user.user_id, today)
        if not tasks:
            return "На данный момент нет заданий. Возможно, Ваш клуб не " \
                   "зарегистрирован в системе."
        text = f"🎈 Список заданий для клуба {current_user_club.name}.\n\n"
        counter = 1
        for task in tasks:
            present_id = False
            task_name = task.task_name
            progress = task.progress
            end = task.end
            if task_name in ("exp", "coin", "heart"):
                mpets = MpetsApi(current_user_club.bot_name,
                                 current_user_club.bot_password)
                await mpets.login()
                pet = await mpets.view_profile(current_user.pet_id)
                limits = await get_limits(pet["level"])
                progress = abs((task.end - limits[task_name]) -
                               task.progress)
                end = limits[task_name]
            elif "send" in task_name:
                present_id = task_name.split("_")[-1]
                task_name = task_name.rsplit("_", maxsplit=1)[0]
            elif "get" in task_name:
                present_id = task_name.split("_")[-1]
                task_name = task_name = task_name.rsplit("_", maxsplit=1)[0]
            if progress >= end:
                if present_id and int(present_id) != 0:
                    args = [gifts_name[int(present_id)-1][1], progress, end]
                else:
                    args = [progress, end]
                text += f"{counter}. " + club_completed_tasks_list[task_name].format(*args) + \
                        "Выполнено ✅\n\n "
                counter += 1
            else:
                if present_id and int(present_id) != 0:
                    args = [gifts_name[int(present_id)-1][1], progress, end]
                else:
                    args = [progress, end]
                text += f"{counter}. " + club_tasks_list[task_name].format(*args) \
                        + "\n"
                counter += 1
        return text


@simple_bot_message_handler(club_router, PayloadFilter({"command": "club"}))
async def profile(event: SimpleBotEvent):
    # Информация о клубе/Профиль клуба
    total_tasks = 0
    points = 0
    current_user = event["current_user"]
    user_stats = crud.get_user_stats(current_user.user_id)
    user_club = crud.get_club(current_user.club_id)
    if user_club is None:
        return "Вы не состоите в клубе."
    elif user_club.status == "waiting":
        return f"Игрок {user_club.bot_name} отправил заявку в клуб. Для " \
               f"повторной отправки заявки нажмите на кнопку «Клубные " \
               f"задания»."
    elif user_club.status == "excluded":
        return f"Игрок {user_club.bot_name} был исключён из вашего клуба." \
               f"Нажмите на кнопку «Клубные задания», чтобы узнать подробнее."
    user_club_stats = crud.get_club_stats(current_user.club_id)
    if user_club_stats is None:
        total_tasks = 0
        points = 0
    else:
        total_tasks = user_club_stats.total_tasks
        points = user_club_stats.points
    total_members_in_club = len(crud.get_users_with_club(current_user.club_id))
    await event.answer(f"🏠 Профиль клуба {user_club.name}\n\n" 
                       f"🎄 Набранные очки: {total_tasks} \n" 
                       f"🏵 Фишки: {points} \n" 
                       f"🧸  Участников: {total_members_in_club}\n"
                       f"————\n"
                       f"Вы выполнили: {user_stats.club_tasks} 📋\n"
                       f"Вы набрали: {user_stats.club_points} 🏵\n\n"
                       f"🐾 Зимняя гонка:\n\n"
                       f"0🚩 — 30🎄 — 70🎄 — 160🎄 — 230🎄 — 350🎄 — 510🎄"
                       f" — 620🎄 — 800🎄 — 980🎄 — 1111🎄 — 1239🏁")


@simple_bot_message_handler(club_router,
                            PayloadFilter({"command": "club_rating"}))
async def club_rating(event: SimpleBotEvent):
    # Рейтинг клубов
    current_user, counter, hidden = event["current_user"], 1, False
    clubs = crud.get_clubs_stats()
    text = "🏠 Рейтинг клубов\n\n"
    if not clubs:
        return "Рейтинг пуст"
    for club_stats in clubs:
        # Если клуб уже есть в списке,
        # то его статастика отдельно снизу не пишется
        if current_user.club_id == club_stats.club_id:
            hidden = True
        club = crud.get_club(club_stats.club_id)
        text += f"{counter}. {club.name} — {club_stats.points} 🏵\n"
        counter += 1
    if not hidden:
        current_user_club = crud.get_club(current_user.club_id)
        current_user_club_stats = crud.get_club_stats(current_user.club_id)
        if current_user_club_stats:
            text += f"\n{current_user_club.name} — {current_user_club_stats.points} 🏵\n"
    await event.answer(text)


@simple_bot_message_handler(club_router, TextContainsFilter("+check"))
async def club_rating(event: SimpleBotEvent):
    # Проверить подарок
    current_user = event["current_user"]
    today = int(datetime.today().strftime("%Y%m%d"))
    try:
        pet_id = int(event.object.object.message.text.split(" ")[1])
    except:
        return "Неверно указан id."
    current_user_tasks = crud.get_club_tasks(current_user.user_id, today)
    current_user_club = crud.get_club(current_user.club_id)
    mpets = MpetsApi(current_user_club.bot_name,
                     current_user_club.bot_password)
    await mpets.login()
    profile = await mpets.view_profile(current_user.pet_id)
    if profile["status"] == "error":
        return "Игрок не найден"
    elif int(profile["club_id"]) != current_user_club.club_id:
        return "Вы не состоите в клубе"
    elif not current_user_tasks:
        return "На данный момент нет заданий. Возможно, Ваш клуб не " \
               "зарегистрирован в системе."
    for user_task in current_user_tasks:
        if user_task.task_name == 'completed':
            continue
        elif "send_specific_gift_any_player" in user_task.task_name or \
                "send_gift_any_player" in user_task.task_name:
            if await checking_sendGift_task(mpets, current_user,
                                            user_task, pet_id):
                await event.answer("Задание выполнено")
            else:
                await event.answer("Подарок не найден")
