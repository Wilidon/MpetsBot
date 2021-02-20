import time
from datetime import datetime

from vkwave.bots import DefaultRouter, SimpleBotEvent, \
    simple_bot_message_handler, PayloadFilter

from sql import crud
from utils import functions
from keyboards.kb import menu
from utils.constants import holiday_0214_completed, holiday_0214, holiday_1402, holiday_2302, holiday_0223_completed, \
    holiday_0223

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
async def holiday_handler(event: SimpleBotEvent):
    holiday = False
    text = ""
    current_user = event["current_user"]
    today = int(datetime.today().strftime("%m%d"))
    if holiday_1402[0] <= today <= holiday_1402[1]:
        text = f"🥰 Список заданий ко дню Святого Валентина.\n\n"
        holiday = True
    current_user_tasks = crud.get_user_tasks(current_user.user_id, holiday_1402[2])
    if not current_user_tasks and holiday is True:
        await functions.creation_valentineDay_tasks(user=current_user, date=holiday_1402)
    current_user_tasks = crud.get_user_tasks(current_user.user_id, holiday_1402[2])
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
    # показывает время до конца мероприятия
    today = str(holiday_1402[1] + 1) + datetime.today().strftime("%Y")
    left_time = time.mktime(datetime.strptime(today, "%m%d%Y").timetuple())
    left_time = left_time - int(time.time())
    if left_time > 0:
        text += f"\n До окончания заданий {await timer(left_time)}"
    else:
        text += f"Событие завершилось!"
    await menu(user=current_user, event=event, message=text)


@simple_bot_message_handler(holidays_router,
                            PayloadFilter({"command": "0223"}))
async def holiday_handler(event: SimpleBotEvent):
    holiday = False
    text = ""
    current_user = event["current_user"]
    today = int(datetime.today().strftime("%m%d"))
    if holiday_2302[0] <= today <= holiday_2302[1]:
        text = f"👨‍✈ День защитника Отечества\n\n"
        holiday = True
    current_user_tasks = crud.get_user_tasks(user_id=current_user.user_id, today=holiday_2302[2])
    if not current_user_tasks and holiday is True:
        await functions.creation_defenderDay_tasks(user=current_user, date=holiday_2302)
    current_user_tasks = crud.get_user_tasks(user_id=current_user.user_id, today=holiday_2302[2])
    counter = 1
    for task in current_user_tasks:
        task_name, progress, end = task.task_name, task.progress, task.end
        args = [progress, end]
        if progress >= end:
            task_name = task_name.split("_", maxsplit=1)[0]
            text += f"{counter}. " + holiday_0223_completed[
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
            text += f"{counter}. " + holiday_0223[task_name].format(*args) + "\n"
            counter += 1
    # время до конца мероприятия
    today = str(holiday_2302[1] + 1) + datetime.today().strftime("%Y")
    left_time = time.mktime(datetime.strptime(today, "%m%d%Y").timetuple())
    left_time = int(left_time) - int(time.time())
    if left_time > 0:
        text += f"\n До окончания заданий {await timer(left_time)}"
    else:
        text += f"Событие завершилось!"
    await menu(user=current_user, event=event, message=text)
