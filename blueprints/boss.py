import json
import time
from datetime import datetime

from vkwave.bots import DefaultRouter, SimpleBotEvent, \
    simple_bot_message_handler, PayloadFilter

from config import get_db
from keyboards.kb import menu, boss_kb
from mpetsapi import MpetsApi
from noticed import notice
from sql import crud
from utils.constants import holiday_1402, bosses

boss_router = DefaultRouter()


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


async def left_event():
    # возвращает время до конца мероприятия
    db = get_db()
    date = db.get("boss_end")
    today = str(date + 1) + datetime.today().strftime("%Y")
    left_time = time.mktime(datetime.strptime(today, "%m%d%Y").timetuple())
    left_time = left_time - int(time.time())
    if left_time > 0:
        return f"\n Окончание ивента через {await timer(int(left_time))}"


async def get_user_baff(pet_id: int):
    mpets = MpetsApi(name="Беся53705", password="cyhgdbqzmu")
    resp = await mpets.login()
    if resp['status'] == 'error':
        await mpets.start()
    resp = await mpets.view_profile(pet_id=pet_id)
    if resp['status'] == 'ok':
        return {"status": True,
                "ava_id": resp['ava_id'],
                "about": resp['about']}
    else:
        return {"status": False}


async def get_boss_text(boss):
    if not boss:
        return "Событие завершилось!"
    if len(boss) == 1:
        return f"{bosses[boss[0].boss_id]['name']}\n" \
               f"Осталось: ❤️{boss[0].health_points}\n\n" \
               f"Каждый удар наносит 10 урона\n\n" \
               f"Смена аватарки на «Дракон» +5 урона\n" \
               f"Смена анкеты на «Воюю с драконом!» +5 урона\n" \
               f"{await left_event()}"
    if len(boss) == 2:
        return f"{bosses[boss[0].boss_id]['name']} и {bosses[boss[1].boss_id]['name']}\n" \
               f"Осталось: ❤️{boss[0].health_points} и 💙{boss[1].health_points}\n\n" \
               f"Каждый удар наносит 10 урона\n\n" \
               f"Смена аватарки на «Дракон» +5 урона\n" \
               f"Смена анкеты на «Воюю с драконом!» +5 урона\n" \
               f"{await left_event()}"


@simple_bot_message_handler(boss_router,
                            PayloadFilter({"command": "boss"}))
async def holiday_handler(event: SimpleBotEvent):
    current_user = event["current_user"]
    boss = crud.get_current_boss()
    text = await get_boss_text(boss)
    await boss_kb(user=current_user, event=event, message=text, boss_amount=len(boss))


@simple_bot_message_handler(boss_router,
                            PayloadFilter({"command": "hit1"}) |
                            PayloadFilter({"command": "hit2"}))
async def collect_collection_handler(event: SimpleBotEvent):
    user = event["current_user"]
    try:
        hit_id = json.loads(event.object.object.message.payload)["command"].split("t")[1]
        hit_id = int(hit_id)
    except Exception:
        return "Ошибка"
    amount_damage = 10
    boss_name = "Синий дракон"
    current_bosses = crud.get_current_boss()
    amount_bosses = (len(current_bosses))
    if current_bosses is None:
        text = "Событие завершено"
        await menu(user=user, event=event, message=text)
    if amount_bosses == 1:
        if hit_id == 1:
            boss_name = "Красный дракон"
            id = current_bosses[0].id
            boss_id = current_bosses[0].boss_id
    if amount_bosses == 2:
        if hit_id == 1:
            boss_name = "Красный дракон"
            id = current_bosses[0].id
            boss_id = current_bosses[0].boss_id
        if hit_id == 2:
            boss_name = "Синий дракон"
            id = current_bosses[1].id
            boss_id = current_bosses[1].boss_id
    damage = await get_user_baff(pet_id=user.pet_id)
    if damage['status'] is True:
        if int(damage['ava_id']) == bosses[boss_id]['avatar_id']:
            amount_damage += 5
        if damage['about'] == bosses[boss_id]['about']:
            amount_damage += 5
    crud.create_damage_log(user_id=user.user_id,
                           boss_id=id,
                           damage=amount_damage)
    boss = crud.update_boss_health(boss_id=id,
                                   damage=amount_damage)
    if boss.health_points <= 0:
        crud.update_boss_status(boss_id=id,
                                status="dead")
        text = f"{boss_name} убит! Вы нанесли {amount_damage} ⚔️.\n" \
               f"Ваша награда: ничево"
        notice_msg = f"Босс {boss_name} убит игроком {user.user_id}\n" \
                     f"Его приз: ничево"
        #notice(message=notice_msg)
        amount_bosses -= 1
    else:
        text = await get_boss_text(current_bosses)
        await boss_kb(user=user, event=event, message=text, boss_amount=amount_bosses)
        text = f"Вы нанесли {amount_damage} ⚔️.\n"
    await boss_kb(user=user, event=event, message=text, boss_amount=amount_bosses)


@simple_bot_message_handler(boss_router,
                            PayloadFilter({"command": "kill1"}) |
                            PayloadFilter({"command": "kill2"}))
async def collect_collection_handler(event: SimpleBotEvent):
    user = event["current_user"]
    try:
        kill_id = json.loads(event.object.object.message.payload)["command"].split("t")[1]
        kill_id = int(kill_id)
    except Exception:
        return "Ошибка"
    amount_damage = 10
    current_bosses = crud.get_current_boss()
    if current_bosses is None:
        text = "Событие завершено"
        await menu(user=user, event=event, message=text)
    if len(current_bosses) == 1:
        if kill_id == 1:
            boss_id = current_bosses[0].id
    if len(current_bosses) == 2:
        if kill_id == 1:
            id = current_bosses[0].id
            boss_id = current_bosses[0].boss_id
        if kill_id == 2:
            id = current_bosses[1].id
            boss_id = current_bosses[1].boss_id
    crud.create_damage_log(user_id=user.user_id,
                           boss_id=id,
                           damage=amount_damage)
    crud.update_boss_health(boss_id=id,
                            damage=amount_damage)
    text = f"Вы нанесли {amount_damage} урона."
    await boss_kb(user=user, event=event, message=text, boss_amount=len(current_bosses))
