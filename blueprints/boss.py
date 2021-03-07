import json
import time
from datetime import datetime

from vkwave.bots import DefaultRouter, SimpleBotEvent, \
    simple_bot_message_handler, PayloadFilter

from config import get_db
from keyboards.kb import menu, boss_kb
from mpetsapi import MpetsApi
from sql import crud, models
from utils.constants import holiday_1402, bosses
from utils.functions import notice

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


async def boss_result(boss: models.Boss):
    try:
        clubs_damage = {}
        all_users: list[models.BossRewards] = crud.get_users_boss_reward(boss_id=boss.boss_id)
        user_text = f"Итоги по боссу {bosses[boss.boss_id]['name']}\n" \
                    f"Всего участников: {len(all_users)}\n"
        club_text = f"Итоги по боссу {bosses[boss.boss_id]['name']}\n"
        for user in all_users:
            current_user: models.Users = crud.get_user(user_id=user.user_id)
            try:
                clubs_damage[current_user.club_id] += user.total_damage
            except Exception as e:
                clubs_damage[current_user.club_id] = user.total_damage
            user_text += f"{current_user.first_name} {current_user.last_name} — {user.total_damage} ⚔️"
        for club_id, club_damage in clubs_damage.items():
            club: models.Clubs = crud.get_club(club_id=club_id)
            if club is None:
                continue
            club_text += f"{club.name} — {club_damage} ⚔️"
        return {'user': user_text, 'club': club_text}
    except:
        raise


async def left_event():
    # возвращает время до конца мероприятия
    db = get_db()
    date = db.get("boss_end")
    today = str(date + 1) + datetime.today().strftime("%Y")
    left_time = time.mktime(datetime.strptime(today, "%m%d%Y").timetuple())
    left_time = left_time - int(time.time())
    if left_time > 0:
        return f"\n 🕐 Окончание ивента через {await timer(int(left_time))}"


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


async def get_boss_text(boss, user_id):
    if boss.status == 'dead':
        last_user: models.BossRewards = crud.get_user_killed_boss(boss_id=boss.boss_id)
        user = crud.get_user(user_id=last_user.user_id)
        if last_user.reward == '':
            if user_id == last_user.user_id:
                crud.update_user_boss_reward(user_id=user_id,
                                             boss_id=boss.boss_id,
                                             reward=bosses[boss.boss_id]['reward_killed'])
            else:
                current_user = crud.get_user_boss(user_id=user_id,
                                                  boss_id=boss.boss_id)
                amount = current_user.total_damage // 500
                reward = f"{amount}🌼, {amount*2}🎖, {amount*2}🎈"
                crud.update_user_boss_reward(user_id=user_id,
                                             boss_id=boss.boss_id,
                                             reward=reward)

        if user_id == last_user.user_id:
            return f"{user.name} добил {bosses[boss.boss_id]['short_name']} " \
                   f"и получил {bosses[boss.boss_id]['reward_killed']}.\n\n" \
                   f"💊 Вы нанесли урона: {last_user.total_damage}\n" \
                   f"⚔ Ваша награда: {bosses[boss.boss_id]['reward_killed']}"
        else:
            current_user = crud.get_user_boss(user_id=user_id,
                                              boss_id=boss.boss_id)
            return f"{user.name} добил {bosses[boss.boss_id]['short_name']} " \
                   f"и получил {bosses[boss.boss_id]['reward_killed']}.\n\n" \
                   f"💊 Вы нанесли урона: {last_user.total_damage}\n" \
                   f"⚔ Ваша награда: {current_user.reward}"
    return f"{bosses[boss.boss_id]['name']}\n" \
           f"💊 Осталось: {boss.health_points} ❤\n\n" \
           f"⚔ Каждый удар наносит 10 урона\n\n" \
           f"🐉 Смена аватарки на «Дракон» +5 урона\n" \
           f"🏹 Смена анкеты на «Воюю с драконом!» +5 урона\n" \
           f"{await left_event()}"


@simple_bot_message_handler(boss_router,
                            PayloadFilter({"command": "boss"}))
async def holiday_handler(event: SimpleBotEvent):
    current_user = event["current_user"]
    btn = True
    boss = crud.get_current_boss()
    user_restart = crud.get_user_restart(user_id=current_user.user_id)
    text = await get_boss_text(boss=boss, user_id=current_user.user_id)
    if boss.status == 'dead':
        await menu(user=current_user, event=event, message=text)
        return 0
    if user_restart.time > int(time.time()):
        btn = False
    await boss_kb(user=current_user, event=event, message=text, btn=btn)


@simple_bot_message_handler(boss_router,
                            PayloadFilter({"command": "hit"}))
async def collect_collection_handler(event: SimpleBotEvent):
    user = event["current_user"]
    user_restart = crud.get_user_restart(user_id=user.user_id)
    amount_damage = 10
    current_bosses = crud.get_current_boss()
    if current_bosses.status == 'dead':
        text = await get_boss_text(boss=current_bosses, user_id=user.user_id)
        await menu(user=user, event=event, message=text)
    if user_restart.time > int(time.time()):
        text = f"Ударить можно будет через {await timer(user_restart.time - int(time.time()))}"
        await boss_kb(user=user, event=event, message=text, btn=False)
        return 0
    id = current_bosses.id
    boss_id = current_bosses.boss_id
    boss_name = bosses[boss_id]['name']
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
    crud.update_boss_reward(user_id=user.user_id,
                            boss_id=boss_id,
                            damage=amount_damage)
    if boss.health_points <= 0:
        crud.update_boss_status(boss_id=id,
                                status="dead")
        crud.update_boss_reward_status(user_id=user.user_id,
                                       boss_id=boss_id)
        text = f"{boss_name} убит! \nВы нанесли {amount_damage} ⚔️.\n" \
               f"Ваша награда: {bosses[boss_id]['reward_killed']}"
        notice_msg = f"Босс {boss_name} убит игроком {user.first_name} {user.last_name}\n" \
                     f"Его приз: {bosses[boss_id]['reward_killed']}"
        result = await boss_result(boss)
        user_result = result['user']
        club_result = result['club']
        notice(message=notice_msg)
        notice(message=user_result)
        notice(message=club_result)
        await menu(user=user, event=event, message=text)
        return 0
    else:
        last_attack = False
        user_restart = crud.get_user_restart(user_id=user.user_id)
        if user_restart.amount == 4:
            crud.update_boss_restart(user_id=user.user_id,
                                     amount=0)
            crud.update_boss_restart_time(user_id=user.user_id,
                                          time=int(time.time()) + 7200)
            last_attack = True
        else:
            crud.update_boss_restart(user_id=user.user_id,
                                     amount=user_restart.amount+1)
        text = await get_boss_text(boss=current_bosses, user_id=user.user_id)
        await boss_kb(user=user, event=event, message=text)
        if last_attack is True:
            text = f"Вы нанесли {amount_damage} ⚔️.\n" \
                   f"Ударить можно будет через {await timer(user_restart.time - int(time.time()))}"
        else:
            text = f"Вы нанесли {amount_damage} ⚔️.\n"
        await boss_kb(user=user, event=event, message=text, btn=not last_attack)


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
