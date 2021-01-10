import random
import time
from datetime import datetime, timedelta
import copy

import requests
from loguru import logger
from vkwave.bots import SimpleLongPollBot

from config import get_settings
from mpetsapi import MpetsApi
from sql import crud
from tzlocal import get_localzone

from utils.constants import MENU_S

user_tasks = [["avatar"], ["anketa"], ["30online"], ["in_online"]]

user_tasks_list = {"avatar": "Поставить аватар {} на 1 час.\n "
                             "📈 Прогресс: {} из {} \n"
                             "🎖 Награда: 1 ⭐ и 1-3 🏮\n",
                   "anketa": "Сменить данные в «О себе» на 30 минут.\n "
                             "📈 Прогресс: {} из {} \n"
                             "🎖 Награда: 1 ⭐ и 1-3 🏮\n",
                   "30online": "Не выходить из онлайна 30 минут.\n "
                               "📈 Прогресс: {} из {} \n"
                               "🎖 Награда: 1 ⭐ и 1-3 🏮\n",
                   "in_online": "Войти в игру в {} по МСК.\n "
                                "📈 Прогресс: {} из {} \n"
                                "🎖 Награда: 1 ⭐ и 1-3 🏮\n",
                   }

user_completed_tasks_list = {"avatar": "Поставить аватар {}\n",
                             "anketa": "Сменить данные в «О себе»\n",
                             "30online": "Не выходить из онлайна 30 минут\n",
                             "in_online": "Войти в игру в {} по МСК\n", }

club_tasks = ["exp", "heart", "coin",
              "get_gift",
              "get_random_gift",
              "send_specific_gift_any_player",
              "send_gift_any_player",
              # ["send_gift_player"],
              # ["send_specific_gift_player"],
              # ["chat"],
              # ["play"],
              #"thread",
              "upRank",
              "acceptPlayer"]

club_tasks_list = {"coin": "Пополнить копилку монетами\n"
                           "📈 Прогресс: {} из {}. \n"
                           "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "heart": "Пополнить копилку сердцами\n"
                            "📈 Прогресс: {} из {}.\n"
                            "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "exp": "Набрать опыт\n"
                          "📈 Прогресс: {} из {}\n"
                          "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "get_gift": "Получить подарок «{}» от любого игрока\n"
                               "📈 Прогресс: {} из {}\n"
                               "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "get_random_gift": "Получить любой подарок от любого игрока\n"
                                      "📈 Прогресс: {} из {}\n"
                                      "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "send_specific_gift_any_player": "Отправить подарок «{}» "
                                                    "любому игроку\n"
                                                    "📈 Прогресс: {} из {}\n"
                                                    "🎖 Награда: 1 🎄 и 1-3 🏵\n"
                                                    "\nКогда игрок принял "
                                                    "подарок, для проверки "
                                                    "отправьте +check 1, "
                                                    "где 1 — id игрока\n\n",
                   "send_gift_any_player": "Отправить любой подарок любому "
                                           "игроку. \n "
                                           "📈 Прогресс: {} из {}. \n"
                                           "🎖 Награда: 1 🎄 и 1-3 🏵\n"
                                           "\nКогда игрок принял "
                                           "подарок, для проверки "
                                           "отправьте +check 1, "
                                           "где 1 — id игрока.\n\n",
                   "send_gift_player": "Отправить любой подарок игроку {}. \n "
                                       "📈 Прогресс: {} из {}. \n"
                                       "🎖 Награда: 1 🎄\n",
                   "send_specific_gift_player": "Отправить подарок {} игроку {}.\n"
                                                "📈 Прогресс: {} из {}. \n"
                                                "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "chat": "Отправить любое сообщение в клубной чат. \n "
                           "📈 Прогресс: {} из {}. \n"
                           "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "play": "Сыграть в Поиграйку (Выполнить задание невозможно). \n "
                           "📈 Прогресс: {} из {}. \n"
                           "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "thread": "Написать сообщение в топике вашего клуба "
                             "на гостевом форуме \n "
                             "📈 Прогресс: {} из {}. \n"
                             "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "upRank": "Повысить любого игрока в клубе \n "
                             "📈 Прогресс: {} из {}. \n"
                             "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   "acceptPlayer": "Принять в клуб любого игрока. \n "
                                   "📈 Прогресс: {} из {}. \n"
                                   "🎖 Награда: 1 🎄 и 1-3 🏵\n",
                   }

club_completed_tasks_list = {"coin": "Пополнить копилку монетами. \n",
                             "heart": "Пополнить копилку сердцами. \n",
                             "exp": "Набрать опыт. \n",
                             "get_gift": "Получить подарок {} от любого игрока. \n",
                             "get_random_gift": "Получить подарок от другого "
                                                "игрока. \n",
                             "send_specific_gift_any_player": "Отправить подарок "
                                                              "{} любому "
                                                              "игроку.\n",
                             "send_gift_any_player": "Отправить любой подарок "
                                                     "любому игроку.\n",
                             "send_gift_player": "Отправить подарок от игроку {}.\n",
                             "send_specific_gift_player": "Отправить подарок {} "
                                                          "игроку {}.\n",
                             "send_gift": "Отправить подарок другому игроку. \n",
                             "chat": "Отправить любое сообщение в клубной чат. \n",
                             "play": "Сыграть в Поиграйку (Форум Клубы). \n",
                             "thread": "Написать сообщение в топике "
                                       "вашего клуба на гостевом форуме\n",
                             "upRank": "Повысить любого игрока в клубе. \n",
                             "acceptPlayer": "Принять в клуб любого игрока. \n"}

gifts_name = [[1, "🍓Клубничка"], [2, "🦋Бабочка"],
              [3, "🧳 Чемодан с деньгами"],
              [4, "🐰Ушки зайки"], [5, "💍 Кольцо в ракушке"],
              [6, "🍹Апельсиновый сок"], [7, "🥥 Кокосовый сок"],
              [8, "🌹 Букет роз"], [9, "🏝 Остров"],
              [10, "🥤Лимонад с семечками"],
              [11, "💘Сердечко"], [12, "🐿Скрат"],
              [13, "⚽️Футбольный мяч"], [14, "☕️ Кофе"], [15, "🏍 Мотоцикл"],
              [16, "🍨Мороженое"], [17, "🧸Влюблённые мишки"],
              [18, "🐇Игрушечный зайчик"],
              [19, "🚢 Корабль"], [20, "🍕Пицца"], [21, "🎐Ёлочный шарик"],
              [22, "🎄Ёлочка"],
              [23, "⛄️Снеговик"], [24, "🎅Дед Мороз"],
              [25, "🍷Бутылка вина"], [26, "🚂Танк"],
              [27, "👨🏻‍✈️Шляпа офицера"],
              [28, "🥮Тортик в виде сердца"],
              [29, "🎂Праздничный торт"], [30, "💍Кольцо"],
              [31, "🐭Мышка в мешке"], [32, "🥢Волшебная палочка"],
              [33, "🧙🏻‍♀️Шляпа колдуньи"],
              [34, "👼Ангел Амур"], [35, "🕵🏻‍♀️Девушка"], [45, "🌼Ромашка"],
              [46, "🍫Шоколадка"],
              [47, "🐈Рыжий котик"], [48, "🍋Чай с лимоном"],
              [49, "🐱Манэки-нэко"],
              [50, "🐲Монстрик"],
              [51, "🦝 Енотик"], [52, "🚗 Машина"]]

avatar_name = [[0, "Кошечка"], [1, "Котенок"], [3, "Игривая кошечка"],
               [4, "Влюбленный котик"], [5, "Игривый котик"],
               [6, "Сиамская кошечка"], [7, "Британский котик"],
               [8, "Влюбленная кошечка"], [9, "Лисичка"],
               [10, "Хомячок"], [11, "Дракончик"], [12, "Щенок"],
               [13, "Собачка"], [16, "Сова"], [17, "Панда"],
               [18, "Кролик"], [19, "Тигренок"], [20, "Черепашка"]]

prizes = {10: "Монетка удачи",
          25: "200 монет",
          40: "5m ❤️",
          70: "25 золотых перьев и 5 ⭐️",
          100: "shop_1",
          125: "shop_2",
          160: "500 монет",
          177: "shop_3"}

c_prizes = {30: "2 ⭐️ всем участвующим",
            70: "300 монет в копилку клуба",
            160: "200k опыта",
            230: "5m сердечек в копилку клуба и по 5 👼 всем участвующим",
            350: "15 🎄 и 5 🏵",
            510: "1 ключ и по 15 серебра всем участвующим",
            620: "10m сердечек",
            800: "2’000 монет",
            980: "по 1 шестерни и по 1 монетке удачи  всем участвующим",
            1111: "400k опыта в копилку, 15m сердец и подарки всем "
                  "участвующим",
            1239: "2 🔑 и 10 фишек"}

shop1 = {"item1": "400 монет",
         "item2": "2 волшебных шестерни",
         "item3": "25 ангелов"}
shop2 = {"item1": "аватарка",
         "item2": "35 серебра",
         "item3": "4 монетки удачи"}
shop3 = {"item1": "600 монет",
         "item2": "16m сердец",
         "item3": "6 шестерней"}


async def get_limits(level):
    if 12 <= level <= 18:
        return {"coin": 3, "heart": 500, "exp": 1000}
    elif 19 <= level <= 25:
        return {"coin": 4, "heart": 800, "exp": 2000}
    elif 26 <= level <= 30:
        return {"coin": 5, "heart": 1500, "exp": 5000}
    elif 31 <= level <= 35:
        return {"coin": 6, "heart": 3000, "exp": 10000}
    elif 36 <= level <= 40:
        return {"coin": 7, "heart": 8000, "exp": 15000}
    elif 41 <= level <= 45:
        return {"coin": 8, "heart": 10000, "exp": 30000}
    elif 46 <= level <= 49:
        return {"coin": 9, "heart": 15000, "exp": 50000}
    elif level == 50:
        return {"coin": 10, "heart": 30000, "exp": 100000}


def get_next_utc_unix_00_00():
    DAY = timedelta(1)
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    t = now.replace(tzinfo=None) + DAY
    t = str(t).split(" ")[0]
    t += " 00:00:00"
    next_utc = int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    return next_utc


async def coin_task(user_id, pet_id, club_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    club = crud.get_club(club_id)
    mpets = MpetsApi(club.bot_name, club.bot_password)
    resp = await mpets.login()
    if resp["status"] == "error":
        # logging
        return 0
    pet = await mpets.view_profile(pet_id)
    if pet["status"] == "error":
        # loggin
        return 0
    progress = pet["club_coin"]
    level = await mpets.view_profile(pet_id)
    limits = await get_limits(level["level"])
    end = progress + limits["coin"]
    crud.create_club_task_for_user(user_id=user_id, task_name="coin",
                                   progress=progress, end=end, date=today)


async def heart_task(user_id, pet_id, club_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    club = crud.get_club(club_id)
    mpets = MpetsApi(club.bot_name, club.bot_password)
    resp = await mpets.login()
    if resp["status"] == "error":
        # logging
        return 0
    page, progress, step, counter = 1, 0, True, 0
    while step:
        try:
            pets = await mpets.club_budget_history_all(club_id, 2, page)
            if not pets["players"]:
                break
            for pet in pets["players"]:
                if pet["pet_id"] == pet_id:
                    progress = pet["count"]
                    step = False
                    break
            page += 1
        except:
            counter += 1
            if counter >= 5:
                return 0
    level = await mpets.view_profile(pet_id)
    limits = await get_limits(level["level"])
    end = int(progress) + limits["heart"]
    crud.create_club_task_for_user(user_id=user_id, task_name="heart",
                                   progress=progress, end=end, date=today)


async def exp_task(user_id, pet_id, club_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    club = crud.get_club(club_id)
    mpets = MpetsApi(club.bot_name, club.bot_password)
    resp = await mpets.login()
    if resp["status"] == "error":
        # logging
        return 0
    page, progress, step, counter = 1, 0, True, 0
    while step:
        try:
            pets = await mpets.club_budget_history_all(club_id, 3, page)
            if not pets["players"]:
                break
            for pet in pets["players"]:
                if pet["pet_id"] == pet_id:
                    progress = pet["count"]
                    step = False
                    break
            page +=1
        except:
            counter += 1
            if counter >= 5:
                return 0
    level = await mpets.view_profile(pet_id)
    limits = await get_limits(level["level"])
    end = int(progress) + limits["exp"]
    crud.create_club_task_for_user(user_id=user_id, task_name="exp",
                                   progress=progress, end=end, date=today)


async def get_gift_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    present_id = gifts_name.index(random.choice(gifts_name))
    task_name = "get_gift_" + str(present_id)
    crud.create_club_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def get_random_gift_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    task_name = "get_random_gift_0"
    crud.create_club_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def send_specific_gift_any_player_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    present_id = gifts_name.index(random.choice(gifts_name))
    task_name = "send_specific_gift_any_player_" + str(present_id)
    crud.create_club_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def send_gift_any_player_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    task_name = "send_gift_any_player_0"
    crud.create_club_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def send_gift_player_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    # todo
    crud.create_club_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def send_specific_gift_player_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    # todo
    crud.create_club_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def chat_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="chat",
                                   progress=0, end=1, date=today)


async def play_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="play",
                                   progress=0, end=5, date=today)


async def thread_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="thread",
                                   progress=0, end=1, date=today)


async def upRank_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="upRank",
                                   progress=0, end=1, date=today)


async def acceptPlayer_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="acceptPlayer",
                                   progress=0, end=1, date=today)


async def check_level_pet(pet_id):
    mpets = MpetsApi()
    await mpets.start()
    return await mpets.view_profile(pet_id)


async def get_task_name(task_name):
    if "send" in task_name:
        return task_name.rsplit("_", maxsplit=1)[0]
    elif "get" in task_name:
        present_id = task_name.split("_")[-1]
        return task_name.rsplit("_", maxsplit=1)[0]
    else:
        return task_name


async def creation_club_tasks(club_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    users = crud.get_users_with_club(club_id)
    for user in users:
        c = 0
        all_tasks = crud.get_club_tasks(user.user_id, today)
        local_tasks = copy.deepcopy(club_tasks)
        if all_tasks:
            if len(all_tasks) < 3:
                c = len(all_tasks)
                for task in all_tasks:
                    task_name = await get_task_name(task.task_name)
                    local_tasks.pop(local_tasks.index(task_name))
            else:
                continue
        while c < 3:
            num = random.randint(0, len(local_tasks) - 1)
            if local_tasks[num] == "coin":
                await coin_task(user.user_id, user.pet_id, club_id)
            elif local_tasks[num] == "heart":
                await heart_task(user.user_id, user.pet_id, club_id)
            elif local_tasks[num] == "exp":
                await exp_task(user.user_id, user.pet_id, club_id)
            elif local_tasks[num] == "get_gift":
                await get_gift_task(user.user_id)
            elif local_tasks[num] == "get_random_gift":
                await get_random_gift_task(user.user_id)
            elif local_tasks[num] == "send_specific_gift_any_player":
                await send_specific_gift_any_player_task(user.user_id)
            elif local_tasks[num] == "send_gift_any_player":
                await send_gift_any_player_task(user.user_id)
            elif local_tasks[num] == "send_gift_player":
                await send_gift_player_task(user.user_id)
            elif local_tasks[num] == "send_specific_gift_player":
                await send_specific_gift_player_task(user.user_id)
            elif local_tasks[num] == "chat":
                await chat_task(user.user_id)
            elif local_tasks[num] == "play":
                await play_task(user.user_id)
            elif local_tasks[num] == "thread":
                await thread_task(user.user_id)
            elif local_tasks[num] == "upRank":
                profile = await check_level_pet(user.pet_id)
                if profile["status"] == "ok" and \
                        profile["rank"] in ['Активист', 'Куратор',
                                            'Зам. Директора', 'Директор']:
                    await upRank_task(user.user_id)
                else:
                    continue
            elif local_tasks[num] == "acceptPlayer":
                profile = await check_level_pet(user.pet_id)
                if profile["status"] == "ok" and \
                        profile["rank"] in ['Куратор',
                                            'Зам. Директора', 'Директор']:
                    await acceptPlayer_task(user.user_id)
                else:
                    continue
            c += 1
            local_tasks.pop(num)


async def avatar_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    avatar = avatar_name.index(random.choice(avatar_name))
    task_name = f"avatar_{avatar}:0"
    crud.create_user_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=60, date=today)


async def anketa_task(user_id, pet_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    mpets = MpetsApi()
    await mpets.start()
    profile = await mpets.view_anketa(pet_id)
    if profile["status"] != "ok":
        return 0
    task_name = f"anketa_{profile['about']}:0"
    crud.create_user_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=30, date=today)


async def online_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_user_task_for_user(user_id=user_id, task_name="30online_0",
                                   progress=0, end=30, date=today)


async def in_online_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    m = random.randint(0, 59)
    if m < 10:
        m = "0" + str(m)
    task_name = f"in_online_{random.randint(11, 19)}" \
                f":{m}"
    crud.create_user_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)


async def creation_user_tasks(user):
    today = int(datetime.today().strftime("%Y%m%d"))
    c = 0
    all_tasks = crud.get_user_tasks(user.user_id, today)
    if all_tasks:
        return 0
    local_tasks = copy.deepcopy(user_tasks)
    while c < 3:
        num = random.randint(0, len(local_tasks) - 1)
        if local_tasks[num][0] == "avatar":
            await avatar_task(user.user_id)
        elif local_tasks[num][0] == "anketa":
            await anketa_task(user.user_id, user.pet_id)
        elif local_tasks[num][0] == "30online":
            await online_task(user.user_id)
        elif local_tasks[num][0] == "in_online":
            await in_online_task(user.user_id)
        c += 1
        local_tasks.pop(num)


async def user_prizes(score):
    """
    10 - монетка удачи
    25 - 200 монет
    40 - 5m ❣️
    70 - 25 золотых перьев и 5 ⭐️
    100 - магазин, 1 товар на выбор (400 монет , 2 волшебных шестерни , 25 ангелов )
    125 - магазин, 1 товар на выбор ( аватарка , 35 серебра  , 4 монетки удачи )
    160 - 500 монет
    177 - магазин, 2 товара на выбор ( 600 монет , 16m ❣️, 6 шестерней,
    35 ангелов, 60 серебра, 10 ⭐️)
    """
    if int(score) in [10, 25, 40, 70, 100, 125, 160, 177]:
        return True
    return False


async def club_prizes(score):
    """
    30 - 2 ⭐️ всем участвующим
    70 - 300 монет в копилку клуба
    160 - 200k опыта
    230 - 5m сердечек в копилку клуба и по 5 👼 всем участвующим
    350 - 15 🎄 и 5 фишек
    510 - 1 ключ и по 15 серебра всем участвующим
    620 - 10m сердечек
    800 - 2’000 монет
    980 - по 1 шестерни и по 1 монетке удачи  всем участвующим
    1111 - 400k опыта в копилку, 15m сердец и подарки всем участвующим
    1239 - 2 🔑 и 10 фишек
    """
    if int(score) in [30, 70, 160, 230, 350, 510, 620, 800, 980, 1111, 1239]:
        return True
    return False


def notice(message):
    settings = get_settings()
    r = requests.get(f"https://api.telegram.org/bot"
                     f"{settings.tg_token}/sendMessage",
                     params={"chat_id": settings.chat_id,
                             "text": message})


async def send_user_notice(user_id, score):
    '''
    Поздравляем! Вы набрали 50 ⭐️
    Доступные товары появились в 🏪Магазине.
    '''
    settings = get_settings()
    message = f"Поздравляем! Вы набрали {score} ⭐️\n" \
              f"Вам будет зачислен приз – {prizes[score]}"
    if "shop" in prizes[score]:
        crud.add_user_item(user_id, prizes[score], score, status=prizes[score])
        message = f"Поздравляем! Вы набрали {score} ⭐️\n" \
                  f"Доступные товары появились в 🏪Магазине."
    else:
        crud.add_user_item(user_id, prizes[score], score)
    bot = SimpleLongPollBot(tokens=settings.token, group_id=settings.group_id)
    if int(score) in [100, 125, 177]:
        try:
            await bot.api_context.messages.send(user_id=user_id,
                                                message=message,
                                                random_id=random.randint(1,
                                                                         9999999),
                                                keyboard=MENU_S.get_keyboard())
        except Exception as e:
            text = f"Не смог отправить сообщение пользователю {user_id}\n" \
                   f"Ошибка: {e}"
            notice(text)
    else:
        try:
            await bot.api_context.messages.send(user_id=user_id,
                                                message=message,
                                                random_id=random.randint(1,
                                                                         9999999))
        except Exception as e:
            text = f"Не смог отправить сообщение пользователю {user_id}\n" \
                   f"Ошибка: {e}"
            notice(text)
    user = crud.get_user(user_id)
    text = f"Игрок {user.first_name} {user.last_name} | {user.name} " \
           f"({user.pet_id}) набрал {score} ⭐\n" \
           f"Приз – {prizes[score]}"
    notice(text)


async def send_club_notice(club_id, score):
    users = crud.get_users_with_club(club_id)
    settings = get_settings()
    message = f"Поздравляем! Вы набрали {score} 🎄\n" \
              f"Вам будет зачислен приз – {c_prizes[score]}"
    crud.add_club_item(club_id, c_prizes[score], score)
    for user in users:
        bot = SimpleLongPollBot(tokens=settings.token,
                                group_id=settings.group_id)
        try:
            await bot.api_context.messages.send(user_id=user.user_id,
                                                message=message,
                                                random_id=random.randint(1,
                                                                         9999999))
        except Exception as e:
            text = f"Не смог отправить сообщение пользователю {user.user_id}\n" \
                   f"Ошибка: {e}"
            notice(text)
    club = crud.get_club(club_id)
    text = f"Клуб {club.name} ({club_id}) набрал {score} 🎄\n" \
           f"Приз – {c_prizes[score]}"
    notice(text)


async def add_user_points(user_id, point=True):
    points = 0
    if point:
        points = random.randint(1, 3)
    crud.update_user_stats(user_id, points=points, personal_tasks=1)
    user = crud.get_user(user_id)
    if point:
        text = f"Пользователь {user.name} ({user_id}) заработал "\
               f"{points} 🏮 и 1 ⭐."
        logger.info(text)
        notice(text)
    user_stats = crud.get_user_stats(user_id)
    if await user_prizes(user_stats.personal_tasks):
        await send_user_notice(user_id, user_stats.personal_tasks)


async def add_club_points(user_id=None, club_id=None, point=True):
    points, user_name = 0, None
    if point:
        points = random.randint(1, 3)
    crud.update_club_stats(club_id, points, 1)
    if user_id:
        user = crud.get_user(user_id)
        user_name = user.name
    club = crud.get_club(club_id)
    if point:
        text = f"Пользователь {user_name} ({user_id}) заработал в клуб"\
               f" {club.name} ({club_id}) {points} 🏵 и 1 🎄."
        logger.info(text)
        notice(text)
    if user_id:
        crud.update_user_stats(user_id, club_tasks=1, club_points=points)
    club_stats = crud.get_club_stats(club_id)
    if await club_prizes(club_stats.total_tasks):
        await send_club_notice(club_id, club_stats.total_tasks)
