import random
import time
from datetime import datetime, timedelta
import copy

import pickledb
import requests
from vkwave.bots import SimpleLongPollBot

from config import get_settings, get_db
from mpetsapi import MpetsApi
from sql import crud
from tzlocal import get_localzone

from utils.constants import get_keyboard

month = {"01": "января", "02": "февраля", "03": "марта",
         "04": "апреля", "05": "мая", "06": "июня",
         "07": "июля", "08": "августа", "09": "сентября",
         "10": "октярбря", "11": "ноября", "12": "декабря"}

access_name = {0: "Пользователь",
               1: "VIP-игрок",
               2: "Модератор",
               3: "Администратор"}

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
                   "charm": "Набрать очки в игре «Снежки»\n"
                            "📈 Прогресс: {} из {} \n"
                            "🎖 Награда: 1 ⭐ и 1-3 🏮\n",
                   "races": "Набрать очки в игре «Скачки»\n"
                            "📈 Прогресс: {} из {} \n"
                            "🎖 Награда: 1 ⭐ и 1-3 🏮\n"
                   }
holiday_0214 = {"gifts": "Обменяться подарками из раздела «Праздники: День Св. Валентина» с 15 разными игроками\n"
                        "📈 Прогресс: {} из {}\n"
                        "🎖 Награда: 10 ангелов\n",
                "avatar": "Поставить аватарку на выбор: Влюблённый котик, Влюблённая кошка  на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          "🎖 Награда: 2 ангела \n",
                "anketa": "Поставить «❤️» в анкету на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          "🎖 Награда: 2 ангела\n",
                }

holiday_0214_completed = {
    "gifts": "Обменяться подарками из раздела «Праздники: День Св. Валентина» с 15 разными игроками\n",
    "avatar": "Поставить аватарку на выбор: Влюблённый котик, Влюблённая кошка  на 24 часа\n",
    "anketa": "Поставить «❤️» в анкету на 24 часа\n", }

user_completed_tasks_list = {"avatar": "Поставить аватар {}\n",
                             "anketa": "Сменить данные в «О себе»\n",
                             "30online": "Не выходить из онлайна 30 минут\n",
                             "in_online": "Войти в игру в {} по МСК\n",
                             "charm": "Набрать очки в игре «Снежки»\n",
                             "races": "Набрать очки в игре «Скачки»\n"}

club_tasks = ["exp", "heart", "coin",
              "get_gift",
              "get_random_gift",
              "send_specific_gift_any_player",
              "send_gift_any_player",
              # ["send_gift_player"],
              # ["send_specific_gift_player"],
              # ["chat"],
              "play",
              # "thread",
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
                   "play": "Сыграть в Поиграйку (Форум Клубы)\n "
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
                             "play": "Сыграть в Поиграйку (Форум Клубы) \n",
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
          160: "400 монет",
          177: "shop_3"}

c_prizes = {30: "2 ⭐️ всем участвующим",
            70: "300 монет в копилку клуба",
            160: "200k опыта",
            230: "5m ❤️ в копилку клуба и по 5 👼 всем участвующим",
            350: "15 🎄 и 5 🏵",
            510: "1 🔑 и по 15 серебра всем участвующим",
            620: "10m ❤️",
            800: "2’000 монет",
            980: "по 1 ⚙️ и по 1 монетке удачи всем участвующим",
            1111: "400k опыта в копилку, 15m ❤️ и 1 🎁 всем участвующимучаствующим",
            1239: "2 🔑 и 10 фишек"}

shop1 = {"item1": "300 монет",
         "item2": "2 волшебных шестерни",
         "item3": "20 ангелов"}
shop2 = {"item1": "17 серебра",
         "item2": "5m ❤️",
         "item3": "2 монетки удачи",
         "item4": "13 ангелов"}
shop3 = {"item1": "15🏮",
         "item2": "5m ❤️",
         "item3": "4 ⚙️",
         "item4": "10 👼",
         "item5": "15 🍿 ",
         "imte6": "5 ⭐️"}


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
    day = timedelta(1)
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    t = now.replace(tzinfo=None) + day
    t = str(t).split(" ")[0]
    t += " 00:00:00"
    next_utc = int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    return next_utc


async def coin_task(task, pet_id, club_id):
    try:
        today = int(datetime.today().strftime("%Y%m%d"))
        club = crud.get_club(club_id)
        mpets = MpetsApi(club.bot_name, club.bot_password)
        resp = await mpets.login()
        if resp["status"] == "error":
            # logging
            return False
        pet = await mpets.view_profile(pet_id)
        if pet["status"] == "error":
            # loggin
            return False
        progress = pet["club_coin"]
        level = await mpets.view_profile(pet_id)
        limits = await get_limits(level["level"])
        end = progress + limits["coin"]
        crud.update_club_task_v2(id=task.id, task_name="coin",
                                 progress=progress, end=end, date=today)
        return True
    except Exception:
        return False


async def heart_task(task, pet_id, club_id):
    try:
        today = int(datetime.today().strftime("%Y%m%d"))
        club = crud.get_club(club_id)
        mpets = MpetsApi(club.bot_name, club.bot_password)
        resp = await mpets.login()
        if resp["status"] == "error":
            # logging
            return False
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
            except Exception:
                counter += 1
                if counter >= 5:
                    return False
        level = await mpets.view_profile(pet_id)
        limits = await get_limits(level["level"])
        end = int(progress) + limits["heart"]
        crud.update_club_task_v2(id=task.id, task_name="heart",
                                 progress=progress, end=end, date=today)
        return True
    except Exception:
        return False


async def exp_task(task, pet_id, club_id):
    try:
        today = int(datetime.today().strftime("%Y%m%d"))
        club = crud.get_club(club_id)
        mpets = MpetsApi(club.bot_name, club.bot_password)
        resp = await mpets.login()
        if resp["status"] == "error":
            # logging
            return False
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
                page += 1
            except Exception:
                counter += 1
                if counter >= 5:
                    return False
        level = await mpets.view_profile(pet_id)
        limits = await get_limits(level["level"])
        end = int(progress) + limits["exp"]
        crud.update_club_task_v2(id=task.id, task_name="exp",
                                 progress=progress, end=end, date=today)
        return True
    except Exception:
        return False


async def get_gift_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    present_id = gifts_name.index(random.choice(gifts_name))
    task_name = "get_gift_" + str(present_id)
    crud.update_club_task_v2(id=task.id, task_name=task_name,
                             progress=0, end=1, date=today)
    return True


async def get_random_gift_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    task_name = "get_random_gift_0"
    crud.update_club_task_v2(id=task.id, task_name=task_name,
                             progress=0, end=1, date=today)
    return True


async def send_specific_gift_any_player_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    present_id = gifts_name.index(random.choice(gifts_name))
    task_name = "send_specific_gift_any_player_" + str(present_id)
    crud.update_club_task_v2(id=task.id, task_name=task_name,
                             progress=0, end=1, date=today)
    return True


async def send_gift_any_player_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    task_name = "send_gift_any_player_0"
    crud.update_club_task_v2(id=task.id, task_name=task_name,
                             progress=0, end=1, date=today)
    return True


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
    # todo
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="chat",
                                   progress=0, end=1, date=today)


async def play_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.update_club_task_v2(id=task.id, task_name="play",
                             progress=0, end=5, date=today)


async def thread_task(user_id):
    # todo
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_club_task_for_user(user_id=user_id, task_name="thread",
                                   progress=0, end=1, date=today)


async def upRank_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.update_club_task_v2(id=task.id, task_name="upRank",
                             progress=0, end=1, date=today)
    return True


async def acceptPlayer_task(task):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.update_club_task_v2(id=task.id, task_name="acceptPlayer",
                             progress=0, end=1, date=today)
    return True


async def check_level_pet(pet_id):
    mpets = MpetsApi()
    await mpets.start()
    return await mpets.view_profile(pet_id)


async def get_task_name(task_name):
    if "send" in task_name:
        return task_name.rsplit("_", maxsplit=1)[0]
    elif "get" in task_name:
        # present_id = task_name.split("_")[-1]
        return task_name.rsplit("_", maxsplit=1)[0]
    else:
        return task_name


async def creation_club_tasks(user_task):
    c = 0
    db = get_db()
    local_tasks = db.lgetall("club_tasks")
    today = int(datetime.today().strftime("%Y%m%d"))
    all_tasks = crud.get_club_tasks(user_task.user_id, today)
    user = crud.get_user(user_task.user_id)
    if len(all_tasks) < 3:
        for task in all_tasks:
            task_name = await get_task_name(task.task_name)
            try:
                local_tasks.pop(local_tasks.index(task_name))
            except Exception:
                pass
    while c < 1:
        num = random.randint(0, len(local_tasks) - 1)
        if local_tasks[num] == "coin":
            if await coin_task(user_task,
                               user.pet_id, user.club_id) is False:
                continue
        elif local_tasks[num] == "heart":
            if await heart_task(user_task,
                                user.pet_id, user.club_id) is False:
                continue
        elif local_tasks[num] == "exp":
            if await exp_task(user_task,
                              user.pet_id, user.club_id) is False:
                continue
        elif local_tasks[num] == "get_gift":
            if await get_gift_task(user_task) is False:
                continue
        elif local_tasks[num] == "get_random_gift":
            if await get_random_gift_task(user_task) is False:
                continue
        elif local_tasks[num] == "send_specific_gift_any_player":
            if await send_specific_gift_any_player_task(user_task) is False:
                continue
        elif local_tasks[num] == "send_gift_any_player":
            if await send_gift_any_player_task(user_task) is False:
                continue
        elif local_tasks[num] == "send_gift_player":
            if await send_gift_player_task(user_task) is False:
                continue
        elif local_tasks[num] == "send_specific_gift_player":
            if await send_specific_gift_player_task(user_task) is False:
                continue
        elif local_tasks[num] == "chat":
            if await chat_task(user_task) is False:
                continue
        elif local_tasks[num] == "play":
            if await play_task(user_task) is False:
                continue
        elif local_tasks[num] == "thread":
            if await thread_task(user_task) is False:
                continue
        elif local_tasks[num] == "upRank":
            profile = await check_level_pet(user.pet_id)
            if profile["status"] == "ok" and \
                    profile["rank"] in ['Активист', 'Куратор',
                                        'Зам. Директора', 'Директор']:
                if await upRank_task(user_task) is False:
                    continue
            else:
                continue
        elif local_tasks[num] == "acceptPlayer":
            profile = await check_level_pet(user.pet_id)
            if profile["status"] == "ok" and \
                    profile["rank"] in ['Куратор',
                                        'Зам. Директора', 'Директор']:
                if await acceptPlayer_task(user_task) is False:
                    continue
            else:
                continue
        c += 1


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
        return False
    task_name = f"anketa_{profile['about']}:0"
    crud.create_user_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=30, date=today)
    return True


async def online_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    crud.create_user_task_for_user(user_id=user_id, task_name="30online_0",
                                   progress=0, end=30, date=today)


async def in_online_task(user_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    h = int(datetime.today().strftime("%H"))
    end = 24
    if h <= 11:
        h = random.randint(12, 17)
    if h >= 23:
        return False
    m = random.randint(0, 59)
    if m < 10:
        m = "0" + str(m)
    if h + 2 <= 24:
        end = h + 2
    task_name = f"in_online_{random.randint(h + 1, end)}" \
                f":{m}"
    crud.create_user_task_for_user(user_id=user_id, task_name=task_name,
                                   progress=0, end=1, date=today)
    return True


async def charm_task(user_id, pet_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    rating = crud.get_charm_rating(pet_id=pet_id)
    if rating is None:
        return False
    crud.create_user_task_for_user(user_id=user_id, task_name="charm",
                                   progress=rating.score,
                                   end=rating.score + 30, date=today)


async def races_task(user_id, pet_id):
    today = int(datetime.today().strftime("%Y%m%d"))
    rating = crud.get_races_rating(pet_id=pet_id)
    if rating is None:
        return False
    crud.create_user_task_for_user(user_id=user_id, task_name="races",
                                   progress=rating.score,
                                   end=rating.score + 30, date=today)


async def creation_user_tasks(user):
    today = int(datetime.today().strftime("%Y%m%d"))
    c = 0
    all_tasks = crud.get_user_tasks(user.user_id, today)
    if all_tasks:
        return 0
    db = get_db()
    local_tasks = db.lgetall("user_tasks")
    while c < 3:
        num = random.randint(0, len(local_tasks) - 1)
        if local_tasks[num] == "avatar":
            await avatar_task(user.user_id)
        elif local_tasks[num] == "anketa":
            if await anketa_task(user.user_id, user.pet_id) is False:
                continue
        elif local_tasks[num] == "30online":
            await online_task(user.user_id)
        elif local_tasks[num] == "in_online":
            if await in_online_task(user.user_id) is False:
                local_tasks.pop(num)
                continue
        elif local_tasks[num] == "charm":
            if await charm_task(user.user_id, user.pet_id) is False:
                local_tasks.pop(num)
                continue
        elif local_tasks[num] == "races":
            if await races_task(user.user_id, user.pet_id) is False:
                local_tasks.pop(num)
                continue
        c += 1
        local_tasks.pop(num)


async def creation_valentineDay_tasks(user):
    all_tasks = crud.get_user_tasks(user.user_id, 214)
    if all_tasks:
        return False
    avatars = [[8, "Влюбленная кошечка"], [4, "Влюбленный котик"]]
    task_name = f"avatar_{random.choice(avatars)[0]}:0"
    crud.create_user_task_for_user(user_id=user.user_id, task_name=task_name,
                                   progress=0, end=24, date=214)
    task_name = "anketa_1:0"
    crud.create_user_task_for_user(user_id=user.user_id, task_name=task_name,
                                   progress=0, end=24, date=214)
    task_name = "gifts"
    crud.create_user_task_for_user(user_id=user.user_id, task_name=task_name,
                                   progress=0, end=15, date=214)
    return True


async def user_prizes(score):
    """
    10 - 1 Монетка удачи
    25 - 200 монет
    40 - 5m ❣️
    70 - 25 золотых перьев и 5 ⭐️
    100 - магазин, 1 товар на выбор (300 монет, 2 волшебных шестерни, 20 ангелов )
    125 - магазин, 2 товара на выбор ( 17 серебра, 2m ❤️, 2 Монетки удачи, 13 ангелов )
    160 - 400 монет
    177 - магазин, 3 товара на выбор ( 15🏮 , 5m ❤️, 4 ⚙️, 10 👼 , 15 🍿 , 5 ⭐️ )
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
    requests.get(f"https://api.telegram.org/bot"
                 f"{settings.tg_token}/sendMessage",
                 params={"chat_id": settings.chat_id,
                         "text": message})


async def send_user_notice(user_id, score):
    """
    Поздравляем! Вы набрали 50 ⭐️
    Доступные товары появились в 🏪Магазине.
    """
    settings = get_settings()
    message = f"Поздравляем! Вы набрали {score} ⭐️\n" \
              f"Вам будет зачислен приз – {prizes[score]}"
    if "shop" in prizes[score]:
        crud.add_user_item(user_id, prizes[score], score, status=prizes[score])
        message = f"Поздравляем! Вы набрали {score} ⭐️\n" \
                  f"Доступные призы появились в 🏪 Магазине."
    else:
        crud.add_user_item(user_id, prizes[score], score)
    bot = SimpleLongPollBot(tokens=settings.token, group_id=settings.group_id)
    if int(score) in [100, 125, 177]:
        try:
            keyboard = await get_keyboard(shop=True)
            await bot.api_context.messages.send(user_id=user_id,
                                                message=message,
                                                random_id=random.randint(1,
                                                                         9999999),
                                                keyboard=keyboard.get_keyboard())
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


async def add_user_points(user_id, point=True, task_name=None):
    points = 0
    if point:
        points = random.randint(1, 3)
    crud.update_user_stats(user_id, points=points, personal_tasks=1)
    user = crud.get_user(user_id)
    if point:
        text = f"Пользователь {user.name} ({user_id}) заработал " \
               f"{points} 🏮 и 1 ⭐."
        # notice(text)
        crud.create_user_log(user_id, task_name, points, 1, int(time.time()))
    user_stats = crud.get_user_stats(user_id)
    if await user_prizes(user_stats.personal_tasks):
        await send_user_notice(user_id, user_stats.personal_tasks)


async def add_club_points(user_id=None, club_id=None, point=True, task_name=None):
    points, user_name = 0, None
    if point:
        points = random.randint(1, 3)
    crud.update_club_stats(club_id, points, 1)
    if user_id:
        user = crud.get_user(user_id)
        user_name = user.name
    club = crud.get_club(club_id)
    if point:
        text = f"Пользователь {user_name} ({user_id}) заработал в клуб" \
               f" {club.name} ({club_id}) {points} 🏵 и 1 🎄."
        # notice(text)
        crud.create_club_log(user_id, task_name, club_id, points, 1, int(time.time()))
    if user_id:
        crud.update_user_stats(user_id, club_tasks=1, club_points=points)
    club_stats = crud.get_club_stats(club_id)
    if await club_prizes(club_stats.total_tasks):
        await send_club_notice(club_id, club_stats.total_tasks)
