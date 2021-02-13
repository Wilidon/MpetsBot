import time
from datetime import datetime, timedelta

from vkwave.bots import DefaultRouter, SimpleBotEvent, \
    simple_bot_message_handler, PayloadFilter, TextContainsFilter

from mpetsapi import MpetsApi
from sql import crud
from utils import functions
from utils.constants import CONFIRMATION, menu
from utils.functions import notice, holiday_0214_completed, holiday_0214

holidays_router = DefaultRouter()


async def timer(sec):
    if sec > 86400:
        days = sec // 86400
        hours = sec % 86400 // 3600
        return f"{days}д {hours}ч"
    if sec > 3600:
        hours = sec // 3600
        minutes = sec % 3600 // 60
        return str(hours) + 'ч ' + str(minutes) + 'м'
    if 3600 >= sec > 60:
        minutes = sec // 60
        return str(minutes) + 'м'
    if sec <= 60:
        return str(sec) + 'с'


@simple_bot_message_handler(holidays_router,
                            PayloadFilter({"command": "0214"}))
async def holiday(event: SimpleBotEvent):
    holiday = False
    text = ""
    current_user = event["current_user"]
    today = int(datetime.today().strftime("%m%d"))
    if 212 <= today <= 214:
        text = f"🥰 Список заданий ко дню Святого Валентина.\n\n"
        holiday = True
    current_user_tasks = crud.get_user_tasks(current_user.user_id, 214)
    if not current_user_tasks and holiday is True:
        await functions.creation_valentineDay_tasks(current_user)
    current_user_tasks = crud.get_user_tasks(current_user.user_id, 214)
    counter = 1
    for task in current_user_tasks:
        task_name, progress, end = task.task_name, task.progress, task.end
        args = [progress, end]
        if progress >= end:
            task_name = task_name.split("_", maxsplit=1)[0]
            text += f"{counter}. " + holiday_0214_completed[
                task_name].format(*args) + "Выполнено ✅\n\n "
            counter += 1
        else:
            if "avatar" in task_name or "anketa" in task_name:
                sec = task_name.split("_", maxsplit=1)[-1]
                start_time = sec.rsplit(":", maxsplit=1)[1]
                left_time = int(time.time()) - int(start_time)
                if left_time >= 86400:
                    pass
                elif left_time <= 3600:
                    progress = await timer(left_time)
            args = [progress, end]
            task_name = task_name.split("_", maxsplit=1)[0]
            text += f"{counter}. " + holiday_0214[task_name].format(*args) + "\n"
            counter += 1
    left_time = 1613422800 - int(time.time())
    if left_time > 0:
        text += f"\n До окончания заданий {await timer(left_time)}"
    else:
        text += f"Событие завершилось!"
    await menu(user=current_user, event=event, message=text)
