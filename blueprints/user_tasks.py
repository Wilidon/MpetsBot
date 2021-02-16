from datetime import datetime

from loguru import logger
from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter,
)

from sql import crud
from utils import functions
from utils.constants import menu
from utils.functions import user_tasks_list, avatar_name, \
    user_completed_tasks_list

user_router = DefaultRouter()


@simple_bot_message_handler(user_router,
                            PayloadFilter({"command": "user_tasks"}))
async def user_tasks(event: SimpleBotEvent):
    # Список заданий пользователя
    current_user = event["current_user"]
    today = int(datetime.today().strftime("%Y%m%d"))
    current_user_tasks = crud.get_user_tasks(current_user.user_id, today)
    if not current_user_tasks:
        crud.close_all_user_tasks(current_user.user_id)
        await functions.creation_user_tasks(current_user)
    current_user_tasks = crud.get_user_tasks(current_user.user_id, today)
    text = f"🎈 Список заданий для {current_user.name}.\n\n"
    counter = 1
    for task in current_user_tasks:
        task_name, progress, end = task.task_name, task.progress, task.end
        if "avatar" in task_name or "in_online" in task_name:
            if "avatar" in task_name:
                arg = task_name.split("_", maxsplit=1)[-1]
                arg = arg.rsplit(":", maxsplit=1)[0]
                arg = avatar_name[int(arg)][1]
            else:
                arg = task_name.split("_")[-1]
            args = [arg, progress, end]
        else:
            if task_name in ["charm", "races"]:
                if task_name in "charm":
                    rating = crud.get_charm_rating(pet_id=current_user.pet_id)
                if task_name in "races":
                    rating = crud.get_races_rating(pet_id=current_user.pet_id)
                if end - progress > 30:
                    args = [rating.score, 0, 30 + ((end - progress) - 30)]
                else:
                    args = [rating.score, 30 - (end - progress), 30, ]
            else:
                args = [progress, end]
        if progress >= end:
            if "in_online" in task_name:
                task_name = task_name.rsplit("_", maxsplit=1)[0]
            else:
                task_name = task_name.split("_", maxsplit=1)[0]
            text += f"{counter}. " + user_completed_tasks_list[
                task_name].format(*args) + "Выполнено ✅\n\n "
            counter += 1
        else:
            if "in_online" in task_name:
                task_name = task_name.rsplit("_", maxsplit=1)[0]
            else:
                task_name = task_name.split("_", maxsplit=1)[0]
            text += f"{counter}. " + user_tasks_list[task_name].format(*args) \
                    + "\n"
            counter += 1
    await menu(user=current_user, event=event, message=text)


@simple_bot_message_handler(user_router,
                            PayloadFilter({"command": "user_rating"}))
async def user_rating(event: SimpleBotEvent):
    # Рейтинг пользователей
    current_user, counter, hidden = event["current_user"], 1, False
    top_users_stats = crud.get_users_stats_order_by_points(limit=10)
    text = "🧑‍ Рейтинг игроков \n\n"
    if not top_users_stats:
        return "Рейтинг пуст"
    for user_stats in top_users_stats:
        # Если пользователь уже есть в списке, 
        # то его статистика отдельно снизу не пишется
        if current_user.user_id == user_stats.user_id:
            hidden = True
        top_user = crud.get_user(user_stats.user_id)
        text += f"{counter}. {top_user.name} — {user_stats.points} 🏅\n"
        counter += 1
    if not hidden:
        current_user_stats = crud.get_user_stats(current_user.user_id)
        text += f"\n{current_user.name} — {current_user_stats.points} 🏅\n"
    await menu(user=current_user, event=event, message=text)


@simple_bot_message_handler(user_router,
                            PayloadFilter({"command": "profile"}))
async def profile(event: SimpleBotEvent):
    # Профиль пользователя
    current_user = event["current_user"]
    club_name = False
    current_user_stats = crud.get_user_stats(current_user.user_id)
    current_user_club = crud.get_club(current_user.club_id)
    if current_user_club:
        club_name = current_user_club.name
        text = f"🧸 Ваш профиль:\n" \
               f"🧩 ID: {current_user.id} / {current_user.pet_id}\n" \
               f"👨🏼‍💼 Имя: {current_user.name}\n" \
               f"🏠 Клуб: {club_name}\n" \
               f"🏅 Медалей: {current_user_stats.points}\n" \
               f"⭐ Набрано звездочек: {current_user_stats.personal_tasks}\n" \
               f"📈 Выполнено личных заданий: {current_user_stats.personal_tasks}\n" \
               f"🕛 Дата регистрации: " \
               f"{datetime.fromtimestamp(current_user.created_at)}\n\n" \
               f"🐾 Зимняя гонка:\n\n" \
               f"0🚩— 10⭐ — 25⭐ — 40⭐ — 70⭐ — 100⭐ — 125⭐ — 160⭐ — 177⭐🏁"
    else:
        text = f"🧸 Ваш профиль:\n" \
               f"🧩 ID: {current_user.id} / {current_user.pet_id}\n" \
               f"👨🏼‍💼 Имя: {current_user.name}\n" \
               f"🏅 Медалей: {current_user_stats.points}\n" \
               f"⭐ Набрано звездочек: {current_user_stats.personal_tasks}\n" \
               f"📈 Выполнено личных заданий: {current_user_stats.personal_tasks}\n" \
               f"🕛 Дата регистрации: " \
               f"{datetime.fromtimestamp(current_user.created_at)}\n\n" \
               f"🐾 Зимняя гонка:\n\n" \
               f"0🚩— 10⭐ — 25⭐ — 40⭐ — 70⭐ — 100⭐ — 125⭐ — 160⭐ — 177⭐🏁"

    await menu(user=current_user, event=event, message=text)
