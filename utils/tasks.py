import asyncio
from datetime import datetime
import time

from loguru import logger

from config import get_settings
from mpetsapi import MpetsApi
from sql import crud
from utils import functions
from utils.functions import get_next_utc_unix_00_00, gifts_name


async def checking_coin_task(mpets, user, user_task):
    pet = await mpets.view_profile(user.pet_id)
    if pet["status"] == "error":
        # logging
        return 0
    if pet["club_coin"] is None:
        # logging
        return 0
    progress = pet["club_coin"]
    if user_task.end <= progress:
        crud.update_club_task(user_task.id, user_task.end,
                              "completed")
        await functions.add_club_points(user.user_id, user.club_id)
    else:
        crud.update_club_task(user_task.id, progress)


async def checking_heart_task(mpets, user, user_task):
    page, progress, step, counter = 1, 0, True, 0
    while step:
        try:
            pets = await mpets.club_budget_history_all(
                user.club_id, 2, page)
            if not pets["players"]:
                break
            for pet in pets["players"]:
                if pet["pet_id"] == user.pet_id:
                    progress = pet["count"]
                    step = False
                    break
            page +=1
        except:
            counter += 1
            if counter >= 5:
                return 0
    if user_task.end <= int(progress):
        crud.update_club_task(user_task.id, user_task.end,
                              "completed")
        await functions.add_club_points(user.user_id, user.club_id)
    else:
        crud.update_club_task(user_task.id, progress)


async def checking_exp_task(mpets, user, user_task):
    page, progress, step, counter = 1, 0, True, 0
    while step:
        try:
            pets = await mpets.club_budget_history_all(
                user.club_id, 3, page)
            if not pets["players"]:
                break
            for pet in pets["players"]:
                if pet["pet_id"] == user.pet_id:
                    progress = pet["count"]
                    step = False
                    break
            page +=1
        except:
            counter += 1
            if counter >= 5:
                return 0
    if user_task.end <= progress:
        crud.update_club_task(user_task.id, user_task.end,
                              "completed")
        await functions.add_club_points(user.user_id, user.club_id)
    else:
        crud.update_club_task(user_task.id, progress)


async def checking_getGift_task(mpets, user, user_task):
    gift_id = user_task.task_name.split("_")[-1]
    pet_gift = False
    if gift_id.isdigit() is False:
        return 0
    gifts = await mpets.view_gifts(user.pet_id)
    if int(gift_id) == 0:
        for gift in gifts["players"]:
            if "сегодня" in gift["date"]:
                pet_gift = True
        if pet_gift:
            crud.update_club_task(user_task.id, user_task.end,
                                    "completed")
            await functions.add_club_points(user.user_id, user.club_id)
    else:
        gift_id = int(gifts_name[int(gift_id) - 1][0])
        for gift in gifts["players"]:
            if gift_id in [26, 27, 35]:
                if "сегодня" in gift["date"] and \
                        int(gift["present_id"]) == 36:
                    pet_gift = True
                elif "сегодня" in gift["date"] and \
                        int(gift["present_id"]) == 37:
                    pet_gift = True
                elif "сегодня" in gift["date"] and \
                        int(gift["present_id"]) == 38:
                    pet_gift = True
            else:
                if "сегодня" in gift["date"] and \
                        int(gift["present_id"]) == gift_id:
                    pet_gift = True
        if pet_gift:
            crud.update_club_task(user_task.id, user_task.end,
                                    "completed")
            await functions.add_club_points(user.user_id, user.club_id)


async def checking_sendGift_task(mpets, user, user_task, pet_id):
    gift_id = user_task.task_name.split("_")[-1]
    pet_gift = False
    if gift_id.isdigit() is False:
        return 0
    gifts = await mpets.view_gifts(pet_id)
    if int(gift_id) == 0:
        for gift in gifts["players"]:
            if gift["pet_id"]:
                try:
                    if user.pet_id == int(gift["pet_id"]) and \
                            "сегодня" in gift["date"]:
                        pet_gift = True
                except:
                    pass
        if pet_gift:
            crud.update_club_task(user_task.id, user_task.end,
                                    "completed")
            await functions.add_club_points(user.user_id, user.club_id)
            return True
    else:
        gift_id = int(gifts_name[int(gift_id) - 1][0])
        for gift in gifts["players"]:
            if gift_id in [26, 27, 35]:
                if gift["pet_id"]:
                    try:
                        if "сегодня" in gift["date"] and \
                                int(gift["present_id"]) == 36 and \
                                user.pet_id == int(gift["pet_id"]):
                            pet_gift = True
                        elif "сегодня" in gift["date"] and \
                                int(gift["present_id"]) == 37 and \
                                user.pet_id == int(gift["pet_id"]):
                            pet_gift = True
                        elif "сегодня" in gift["date"] and \
                                int(gift["present_id"]) == 38 and\
                                user.pet_id == int(gift["pet_id"]):
                            pet_gift = True
                    except:
                        pass
            else:
                if gift["pet_id"]:
                    try:
                        if "сегодня" in gift["date"] and \
                                int(gift["present_id"]) == gift_id and \
                                user.pet_id == int(gift["pet_id"]):
                            pet_gift = True
                        pet_gift = True
                    except:
                        pass
        if pet_gift:
            crud.update_club_task(user_task.id, user_task.end,
                                    "completed")
            await functions.add_club_points(user.user_id, user.club_id)
            return True


'''async def checking_gift_task(mpets, ):
    gift_id = user_task.task_name.split("_")[-1]
    if gift_id.isdigit() is False:
        return 0
    gifts = await mpets.view_gifts(user.pet_id)
    if int(gift_id) == 0:
        for gift in gifts["players"]:
            print(gift)
            if "сегодня" in gift["date"]:
                crud.update_club_task(user_task.id, user_task.end,
                                      "completed")
                await functions.add_club_points(user.user_id, user.club_id)
    else:
        for gift in gifts["players"]:
            if "сегодня" in gift["date"] and \
                    int(gift["present_id"]) == int(gift_id):
                crud.update_club_task(user_task.id, user_task.end,
                                      "completed")
                await functions.add_club_points(user.user_id, user.club_id)'''


async def checking_chat_task(mpets, user, user_task):
    today = int(datetime.today().strftime("%Y%m%d"))
    prize = False
    chat = await mpets.chat(user.club_id)
    for msg in chat["messages"]:
        if crud.get_chat_message(user.club_id, user.pet_id, msg["message"],
                                 today):
            crud.update_club_task(user_task.id, user_task.end,
                                  "completed")
            await functions.add_club_points(user.user_id, user.club_id)
        else:
            if crud.get_chat_message(user.club_id, msg["pet_id"],
                                     msg["message"], today) is None:
                crud.create_chat_message(user.club_id, msg["pet_id"],
                                         msg["message"], today)


async def checking_play_task(mpets, user, user_task):
    pass


async def checking_thread_task(mpets, user, user_task):
    forums = await mpets.forums(user.club_id)
    if forums["status"] == "error":
        # logging
        return 0
    progress = user_task.progress
    for i in range(0, 2):
        threads = await mpets.threads(forums["forums_id"][i]["forum_id"])
        if threads["status"] != "ok":
            continue
        for thread in threads["threads"]:
            page = 1
            thread_data = crud.get_thread_messages(thread)
            if not thread_data:
                while True:
                    thread_info = await mpets.thread(thread, page)
                    if thread_info["status"] == "error":
                        break
                    for thread_msg in thread_info["messages"]:
                        crud.create_thread_message(user.club_id,
                                                   thread_msg["pet_id"],
                                                   thread,
                                                   thread_msg["message"],
                                                   page,
                                                   thread_msg["post_date"])
                        if user.pet_id == int(thread_msg["pet_id"]):
                            progress += 1
                    page += 1
            else:
                page = crud.get_last_page_thread(thread).page
                page = int(page)
                while True:
                    thread_info = await mpets.thread(thread, page)
                    if thread_info["status"] == "error":
                        break
                    for thread_msg in thread_info["messages"]:
                        if crud.check_msg(thread, thread_msg["message"],
                                          thread_msg["post_date"],
                                          page) is None:
                            crud.create_thread_message(user.club_id,
                                                       thread_msg["pet_id"],
                                                       thread,
                                                       thread_msg["message"],
                                                       page,
                                                       thread_msg["post_date"])
                            if user.pet_id == int(thread_msg["pet_id"]):
                                progress += 1
                    page += 1
    if user_task.end <= progress:
        crud.update_club_task(user_task.id, user_task.end,
                                "completed")
        await functions.add_club_points(user.user_id, user.club_id)
    else:
        crud.update_club_task(user_task.id, progress)


async def checking_upRank_task(mpets, user, user_task):
    history = await mpets.club_history(user.club_id)
    today = datetime.today().strftime("%d.%m")
    if history["status"] == "error":
        # logging
        return 0
    progress = user_task.progress
    for his in history["history"]:
        '''if crud.check_upRank_history(his["owner_id"], his["member_id"],
                                     his["action"], his["date"]) is None:
            crud.create_upRank_history(user.club_id, his["owner_id"],
                                       his["member_id"], his["action"],
                                       his["date"]) '''
        if user.pet_id == int(his["owner_id"]) and \
                "повысил" in his["action"] and \
                today == his["date"].split(" ")[0]:
            progress += 1
    if user_task.end <= progress:
        crud.update_club_task(user_task.id, user_task.end,
                              "completed")
        await functions.add_club_points(user.user_id, user.club_id)
    else:
        crud.update_club_task(user_task.id, progress)


async def checking_acceptPlayer_task(mpets, user, user_task):
    history = await mpets.club_history(user.club_id)
    today = datetime.today().strftime("%d.%m")
    if history["status"] == "error":
        # logging
        return 0
    progress = user_task.progress
    for his in history["history"]:
        '''if crud.check_acceptPlayer_history(his["owner_id"], his["member_id"],
                                           his["action"], his["date"]) is None:
            crud.create_acceptPlayer_history(user.club_id, his["owner_id"],
                                             his["member_id"], his["action"],
                                             his["date"])'''
        if user.pet_id == int(his["owner_id"]) and \
                "принял" in his["action"] and \
                today == his["date"].split(" ")[0]:
            progress += 1
    if user_task.end <= progress:
        crud.update_club_task(user_task.id, user_task.end,
                              "completed")
        await functions.add_club_points(user.user_id, user.club_id)
    else:
        crud.update_club_task(user_task.id, progress)


async def start_verify_club(club):
    try:
        today = int(datetime.today().strftime("%Y%m%d"))
        mpets = MpetsApi(club.bot_name, club.bot_password)
        await mpets.login()
        profile = await mpets.profile()
        if profile["club"] is None:
            logger.info(f"{club.bot_name} исключен из клуба ({club.club_id}).")
            crud.update_club_status(club.club_id, "excluded")
        users = crud.get_users_with_club(club.club_id)
        for user in users:
            user_tasks = crud.get_club_tasks(user.user_id, today)
            profile = await mpets.view_profile(user.pet_id)
            if int(profile["club_id"]) != club.club_id:
                return 0
            if not user_tasks:
                crud.close_all_club_tasks(club.club_id)
                await functions.creation_club_tasks(club.club_id)
            elif len(user_tasks) < 3:
                await functions.creation_club_tasks(club.club_id)
            for user_task in user_tasks:
                if user_task.status == "completed":
                    continue
                elif user_task.task_name == "coin":
                    await checking_coin_task(mpets, user, user_task)
                elif user_task.task_name == "heart":
                    await checking_heart_task(mpets, user, user_task)
                elif user_task.task_name == "exp":
                    await checking_exp_task(mpets, user, user_task)
                elif "get_gift" in user_task.task_name or \
                        "get_random_gift" in user_task.task_name:
                    await checking_getGift_task(mpets, user, user_task)
                elif "send_gift_player" in user_task.task_name or \
                        "send_specific_gift_player" in user_task.task_name:
                    await checking_sendGift_task(mpets, user, user_task)
                elif user_task.task_name == "chat":
                    await checking_chat_task(mpets, user, user_task)
                elif user_task.task_name == "play":
                    await checking_play_task(mpets, user, user_task)
                elif user_task.task_name == "thread":
                    await checking_thread_task(mpets, user, user_task)
                elif user_task.task_name == "upRank":
                    await checking_upRank_task(mpets, user, user_task)
                elif user_task.task_name == "acceptPlayer":
                    await checking_acceptPlayer_task(mpets, user, user_task)
    except Exception as e:
        log = logger.bind(context=e)
        log.error(f"Не удалось проверить клуб({club.club_id})")


async def start_verify_account(club):
    mpets = MpetsApi(club.bot_name, club.bot_password)
    await mpets.login()
    profile = await mpets.profile()
    if profile and profile["status"] != "ok":
        log = logger.bind(context=profile)
        log.warning("Не удалось получить профиль.")
        return False
    if profile["club"] is not None:
        logger.success(f"Клуб ({club.club_id}) подтвержден.")
        await functions.creation_club_tasks(club.club_id)
        crud.update_club_status(club.club_id, "ok")


async def checking_bots():
    while True:
        try:
            clubs_with_status_ok = crud.get_clubs(status="ok")
            clubs_with_status_waiting = crud.get_clubs(status="waiting")
            tasks = []
            for club in clubs_with_status_ok:
                task = asyncio.create_task(start_verify_club(club))
                tasks.append(task)
            for club in clubs_with_status_waiting:
                task = asyncio.create_task(start_verify_account(club))
                tasks.append(task)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(10)


async def update_user_data():
    settings = get_settings()
    mpets = MpetsApi(settings.bot1, settings.bot_password)
    while True:
        r = await mpets.login()
        if r["status"] == "ok":
            break
        logger.bind(context=r).critical("Не удалось авторизоваться.")
        await asyncio.sleep(10)
    logger.bind(context=r).success("Функция обновления данных пользователей "
                                   "запущена.")
    while True:
        try:
            users = crud.get_users()
            for user in users:
                profile = await mpets.view_profile(user.pet_id)
                if profile['status'] != 'ok':
                    log = logger.bind(context=profile)
                    log.warning(f"Не удалось обновить информацию "
                                f"пользователя {user.user_id}")
                    continue
                crud.update_user_data(user.user_id, profile["pet_id"],
                                      profile["name"], profile["club_id"])
            await asyncio.sleep(120)
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(3)


async def checking_avatar_task(mpets, user, user_task):
    profile = await mpets.view_profile(user.pet_id)
    if profile["status"] != "ok":
        return 0
    left_time = get_next_utc_unix_00_00()
    avatar_id = user_task.task_name.split("_")[-1]
    if int(functions.avatar_name[int(avatar_id)][0]) == int(profile["ava_id"]) \
            and left_time - int(time.time()) < 1800:
        crud.update_user_task(user_task.id, user_task.end, "completed")
        await functions.add_user_points(user.user_id)


async def checking_anketa_task(mpets, user, user_task):
    profile = await mpets.view_anketa(user.pet_id)
    if profile["status"] != "ok":
        return 0
    left_time = get_next_utc_unix_00_00()
    anketa_about = user_task.task_name.split("_")[-1]
    if anketa_about != profile["about"] \
            and left_time - int(time.time()) < 1800:
        crud.update_user_task(user_task.id, user_task.end, "completed")
        await functions.add_user_points(user.user_id)


async def checking_online_task(mpets, user, user_task):
    profile = await mpets.view_profile(user.pet_id)
    if profile["status"] != "ok":
        return 0
    if profile["last_login"] == "online":
        task_name = user_task.task_name
        if int(task_name.split("_")[1]) == 0:
            task_name = "30online_" + str(int(time.time()))
            crud.update_user_task_name(user_task.id, task_name)
            return 0
        else:
            task_name = int(task_name.split("_")[1])
            left_time = time.time() - task_name
            if left_time >= 1800:
                crud.update_user_task(user_task.id, user_task.end, "completed")
                await functions.add_user_points(user.user_id)
            else:
                left_time = int(left_time//60)
                crud.update_user_task(user_task.id, left_time, "waiting")
    else:
        crud.update_user_task(user_task.id, 0, "waiting")
        crud.update_user_task_name(user_task.id, "30online_0")


async def checking_inOnline_task(mpets, user, user_task):
    profile = await mpets.view_profile(user.pet_id)
    if profile["status"] != "ok":
        return 0
    if profile["last_login"] == "online":
        task_name = user_task.task_name
        h, m = task_name.split("_")[-1].split(":")
        current_date = time.strftime("%d %b %Y", time.gmtime(time.time()))
        current_date += f' {h}:{m}'
        unix_time = int(time.mktime(time.strptime(current_date, '%d %b %Y '
                                                             '%H:%M')))
        if unix_time - 60 <= int(time.time()) <= unix_time + 60:
            crud.update_user_task(user_task.id, user_task.end, "completed")
            await functions.add_user_points(user.user_id)
    else:
        # timeout
        pass


async def start_verify_user(user):
    today = int(datetime.today().strftime("%Y%m%d"))
    user_tasks = crud.get_user_tasks(user.user_id, today)
    user_bot = crud.get_bot(user.user_id)
    if user_bot is None:
        mpets = MpetsApi()
        resp = await mpets.start()
        if resp["status"] == "ok":
            user_bot = crud.create_bot(user.user_id, resp["pet_id"],
                            resp["name"], resp["password"])
        else:
            log = logger.bind(context=f"account {resp}")
            log.warning(f"Ошибка при создании бота. Пользователь:"
                        f" {user.user_id}")
            return 0
    if not user_tasks:
        logger.debug(user.user_id)
        crud.close_all_user_tasks(user.user_id)
        await functions.creation_user_tasks(user)
    mpets = MpetsApi(user_bot.name, user_bot.password)
    resp = await mpets.login()
    if resp["status"] != "ok":
        log = logger.bind(context=f"account {resp}")
        log.warning(f"Ошибка при авторизации бота. Пользователь:"
                    f" {user.user_id}")
        mpets = MpetsApi()
        resp = await mpets.login()
        if resp["status"] != "ok":
            return 0
    for user_task in user_tasks:
        if user_task.status == "completed":
            continue
        elif "avatar" in user_task.task_name:
            await checking_avatar_task(mpets, user, user_task)
        elif "anketa" in user_task.task_name:
            await checking_anketa_task(mpets, user, user_task)
        elif "30online" in user_task.task_name:
            await checking_online_task(mpets, user, user_task)
        elif "in_online" in user_task.task_name:
            await checking_inOnline_task(mpets, user, user_task)


async def checking_users_tasks():
    while True:
        try:
            users = crud.get_users_with_status("ok")
            tasks = []
            for user in users:
                task = asyncio.create_task(start_verify_user(user))
                tasks.append(task)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(10)
