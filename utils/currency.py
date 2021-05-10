import bs4
from aiohttp import ClientTimeout, ClientSession
from bs4 import BeautifulSoup

from mpetsapi import MpetsApi


async def thread_popcorn(thread_id, page, cookies):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10)) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread_popcorn(thread_id, page, cookies)
            elif "Сообщений нет" in resp_text:
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            users = resp.find("div", {"class": "thread_content"})
            users = users.find("span", {"style": "color: #4b1a0a;"}).descendants
            players = []
            i = 0
            for user in users:
                if isinstance(user, bs4.element.NavigableString):
                    try:
                        user = int(user)
                        players[-1][1] = user
                    except Exception as e:
                        pass
                elif isinstance(user, bs4.element.Tag):
                    try:
                        pet_id = int(user['href'].split("=")[1])
                        players.append([pet_id, 0])
                    except Exception as e:
                        pass
                elif isinstance(user, str):
                    players[-1][1] = user
            return {'status': 'ok',
                    'users': players}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def parce_popcorn(pet_id, thread_id, mpets):
    cookie = await mpets.get_cookie()
    users = await thread_popcorn(thread_id=thread_id, page=1, cookies=cookie)
    if users['status'] == 'error':
        return False
    for user in users['users']:
        if user[0] == pet_id:
            return user
    return None


async def thread_plus(thread_id, page, cookies):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10)) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread_plus(thread_id, page, cookies)
            elif "Сообщений нет" in resp_text:
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            users = resp.find("div", {"class": "thread_content"})
            users = users.find("div", {"class": "center"}).descendants
            players = []
            for user in users:
                if isinstance(user, bs4.element.Tag):
                    try:
                        if "– " in user.text or "- " in user.text or "— " in user.text:
                            try:
                                score = int(user.text.split("– ")[1].split(" п")[0])
                                players[-1][1] = score
                            except Exception as e:
                                pass
                        else:
                            pet_id = int(user['href'].split("=")[1])
                            players.append([pet_id, 0])
                    except Exception as e:
                        pass
            return {'status': 'ok',
                    'users': players}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def parce_plus(pet_id, thread_id, mpets):
    cookie = await mpets.get_cookie()
    users = await thread_plus(thread_id=thread_id, page=1, cookies=cookie)
    if users['status'] == 'error':
        return False
    for user in users['users']:
        if user[0] == pet_id:
            return user
    return None


async def thread_silver(thread_id, page, cookies):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10)) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread_silver(thread_id, page, cookies)
            elif "Сообщений нет" in resp_text:
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            users = resp.find("div", {"class": "thread_content"})
            users = users.find("div", {"style": "margin-left: 2em"}).descendants
            players = []
            for user in users:
                if isinstance(user, bs4.element.Tag):
                    try:
                        pet_id = int(user['href'].split("=")[1])
                        players.append([pet_id, 0])
                    except Exception as e:
                        pass
                if isinstance(user, bs4.element.NavigableString):
                    try:
                        if "– " in user or "- " in user or "— " in user:
                            try:
                                score = int(user.split("— ")[1].split(" с")[0])
                                players[-1][1] = score
                            except Exception as e:
                                pass
                    except Exception as e:
                        pass
            return {'status': 'ok',
                    'users': players}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def parce_silver(pet_id, thread_id, mpets):
    cookie = await mpets.get_cookie()
    users = await thread_silver(thread_id=thread_id, page=1, cookies=cookie)
    if users['status'] == 'error':
        return False
    for user in users['users']:
        if user[0] == pet_id:
            return user
    return None


async def thread_feather(thread_id, page, cookies):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10)) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread_feather(thread_id, page, cookies)
            elif "Сообщений нет" in resp_text:
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            users = resp.find("div", {"class": "thread_content"})
            users = users.find("div", {"style": "margin-left: 2em"}).descendants
            players = []
            for user in users:
                if isinstance(user, bs4.element.NavigableString):
                    try:
                        name = user.split(" ", maxsplit=3)
                        name = name[-1].rsplit(" ", maxsplit=2)[0]
                        score = int(user.split("- ")[1])
                        players.append([name, score])
                    except Exception as e:
                        pass
            return {'status': 'ok',
                    'users': players}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def parce_feather(name, thread_id, mpets):
    cookie = await mpets.get_cookie()
    users = await thread_feather(thread_id=thread_id, page=1, cookies=cookie)
    if users['status'] == 'error':
        return False
    for user in users['users']:
        if user[0] == name:
            return user
    return None


async def thread_key(thread_id, page, cookies):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10)) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread_key(thread_id, page, cookies)
            elif "Сообщений нет" in resp_text:
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            users = resp.find("div", {"class": "thread_content"})
            users = users.find("div", {"style": "margin-left: 2em"}).descendants
            players = []
            for user in users:
                if isinstance(user, bs4.element.Tag):
                    try:
                        club_id = int(user['href'].split("=")[1])
                        players.append([club_id, 0])
                    except Exception as e:
                        pass
                if isinstance(user, bs4.element.NavigableString):
                    try:
                        if "– " in user or "- " in user or "— " in user:
                            players[-1][1] = int(user.split(" ")[2])
                    except Exception as e:
                        pass
            return {'status': 'ok',
                    'users': players}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def parce_key(club_id, thread_id, mpets):
    cookie = await mpets.get_cookie()
    users = await thread_key(thread_id=thread_id, page=1, cookies=cookie)
    if users['status'] == 'error':
        return False
    for user in users['users']:
        if user[0] == club_id:
            return user
    return None


async def thread_angel(players, thread_id, page, cookies):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10)) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread_angel(players, thread_id, page, cookies)
            elif "Сообщений нет" in resp_text:
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
            users = resp.find("div", {"class": "thread_content"})
            users = users.find_all("div", {"style": "margin-left: 2em"})
            for user2 in users:
                user2 = user2.descendants
                for user in user2:
                    if isinstance(user, bs4.element.Tag):
                        try:
                            pet_id = int(user['href'].split("=")[1])
                            players.append([pet_id, 0])
                        except Exception as e:
                            pass
                    if isinstance(user, bs4.element.NavigableString):
                        try:
                            if "– " in user or "- " in user or "— " in user:
                                if players[-1][1] == 0:
                                    players[-1][1] = int(user.rsplit(" анг")[0].rsplit(" ", maxsplit=1)[-1])
                        except Exception as e:
                            pass
            return {'status': 'ok',
                    'users': players}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def parce_angel(pet_id, thread_ids, mpets):
    cookie = await mpets.get_cookie()
    players = []
    for thread_id in thread_ids:
        users = await thread_angel(players=players, thread_id=thread_id, page=1, cookies=cookie)
    if users['status'] == 'error':
        return False
    for user in users['users']:
        if user[0] == pet_id:
            return user
    return None


async def get_currency(user, event):
    thread_ids = {"popcorn": 2557447,
                  "plus": 2572662,
                  "silver": 2573189,
                  "feather": 2603855,
                  "key": 2570823,
                  "angel": [2501851, 2501843, 2501844, 2501845, 2501846, 2501849,
                            2501856, 2501855, 2501854, 2501853, 2501852, 2531821],
                  "gear": [2531790]}
    pet_id = user.pet_id
    name = user.name
    club_id = user.club_id
    mpets = MpetsApi()
    await mpets.start()

    # ПОПКОРН
    user = await parce_popcorn(pet_id=pet_id,
                               thread_id=thread_ids.get("popcorn"),
                               mpets=mpets)
    if user is None or user is False:
        popcorn = 0
    else:
        popcorn = user[1]

    # ПЛЮСЫ
    user = await parce_plus(pet_id=pet_id,
                            thread_id=thread_ids.get("plus"),
                            mpets=mpets)
    if user is None or user is False:
        plus = 0
    else:
        plus = user[1]

    # СЕРЕБРО

    user = await parce_silver(pet_id=pet_id,
                              thread_id=thread_ids.get("silver"),
                              mpets=mpets)
    if user is None or user is False:
        silver = 0
    else:
        silver = user[1]

    # ЗОЛОТЫЕ ПЕРЬЯ

    user = await parce_feather(name=name,
                               thread_id=thread_ids.get("feather"),
                               mpets=mpets)
    if user is None or user is False:
        feather = 0
    else:
        feather = user[1]

    # СВЯЗКА КЛЮЧЕЙ

    user = await parce_key(club_id=club_id,
                           thread_id=thread_ids.get("key"),
                           mpets=mpets)
    if user is None or user is False:
        key = 0
    else:
        key = user[1]

    # АНГЕЛЫ

    user = await parce_angel(pet_id=pet_id,
                             thread_ids=thread_ids.get("angel"),
                             mpets=mpets)
    if user is None or user is False:
        angel = 0
    else:
        angel = user[1]

    # ШЕСТЕРНИ
    
    '''user = await parce_angel(pet_id=pet_id,
                             thread_ids=thread_ids.get("angel"),
                             mpets=mpets)
    if user is None or user is False:
        angel = 0
    else:
        angel = user[1]'''

    text = "💎 Ваша валюта.\n\n" \
           f"Попкорн: {popcorn} 🍿\n" \
           f"Плюсы: {plus} ➕\n" \
           f"Серебро: {silver} 🔘\n" \
           f"Золотые перья: {feather}\n" \
           f"Связка ключей: {key} 🗝\n" \
           f"Ангелы: {angel} 👼"
    await event.answer(message=text)
