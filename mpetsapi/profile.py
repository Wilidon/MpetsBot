import asyncio
import re

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
import requests_async as requests


async def profile(cookies, timeout, connector):
    try:
        club = rank_club = family_id = family_name = club_const = club_day = effect = None
        last_login = "online"
        prof = await requests.get("http://mpets.mobi/profile", cookies=cookies)
        prof = BeautifulSoup(await prof.read(), 'lxml')
        ava_id = \
            prof.find('img', {'class': 'ava_prof'})['src'].split("avatar")[
                1].split(".")[0]
        name = prof.find("div", {"class": "stat_item"}).text.split(", ")[
            0].replace(' ', '')
        level = prof.find("div", {"class": "stat_item"})
        level = level.find("a",
                           {"class": "darkgreen_link", "href": "/avatars"})
        level = int(
            level.next_element.next_element.split(", ")[1].split(" ")[0])
        rank = prof.find("div", {
            "class": "left font_14 pet_profile_stat"}).find_all("div",
                                                                {
                                                                    "class": "stat_item"})
        i = 0
        for ac in rank:
            if 'Посл. вход:' in ac.text:
                try:
                    last_login = ac.find("span", {''}).text
                except:
                    last_login = ac.find("span", {'c_red'}).text
                last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)
            elif 'VIP-аккаунт' in ac.text:
                effect = ac.text.split(": ")[1].rsplit('  ', maxsplit=1)[0]
            elif 'Премиум-аккаунт' in ac.text:
                effect = ac.text.split(": ")[1].rsplit(' ', maxsplit=1)[0]
            elif 'Семья' in ac.text:
                family_id = int(
                    ac.find("a", {'darkgreen_link'})['href'].split("=")[1])
                family_name = ac.find("a", {'darkgreen_link'}).text
            elif 'Красота' in ac.text:
                beauty = int(ac.text.split(": ")[1])
            elif 'Клуб:' in ac.text:
                club = ac.text.split(": ")[1].split(",")[0]
                rank_club = ac.text.split(", ")[1]
            elif 'Верность клубу' in ac.text:
                club_const = int(ac.text.split(": ")[1].split("%")[0])
            elif 'Дней в клубе:' in ac.text:
                club_day = ac.text.split(": ")[1]
                club_day = int(club_day.split(" ")[0].replace('\t', ''))
            elif 'Дней в игре:' in ac.text:
                day = int(ac.text.split(": ")[1].replace('\t', ''))
            elif 'Монеты:' in ac.text:
                coins = int(ac.text.split(": ")[1].replace('\t', ''))
            elif 'Сердечки:' in ac.text:
                hearts = int(ac.text.split(": ")[1].replace('\t', ''))
            i += 1
        return {'status': 'ok',
                'name': name,
                'level': level,
                'ava_id': ava_id,
                'last_login': last_login,
                'effect': effect,
                'beauty': beauty,
                'coins': coins,
                'hearts': hearts,
                'family_id': family_id,
                'family_name': family_name,
                'club': club,
                'rank': rank_club,
                'club_const': club_const,
                'club_day': club_day,
                'day': day}
    except asyncio.TimeoutError as e:
        return {'status': 'error', 'code': '', 'msg': e}
    except Exception as e:
        return {'status': 'error', 'code': '', 'msg': e}


async def view_profile(pet_id, cookies, connector):
    try:
        club_id = club = rank_club = family_id = family_name = club_const = club_day = effect = None
        last_login = 'online'
        club_coin = club_heart = about = None
        params = {'pet_id': pet_id}
        resp = await requests.get("http://mpets.mobi/view_profile",
                                  params=params,
                                  cookies=cookies)
        prof = BeautifulSoup(await resp.read(), "lxml")
        if "Вы кликаете слишком быстро." in resp.text:
            return await view_profile(pet_id, cookies, connector)
        ava_id = \
            prof.find('img', {'class': 'ava_prof'})['src'].split("avatar")[
                1].split(".")[0]
        name = prof.find("div", {"class": "stat_item"}).text.split(", ")[
            0].replace('\n', '').split(" ", maxsplit=1)[1]
        level = \
            prof.find("div", {"class": "stat_item"}).text.split(", ")[1].split(
                " ")[0]
        rank = prof.find("div", {
            "class": "left font_14 pet_profile_stat"}).find_all("div", {
            "class": "stat_item"})
        for ac in rank:
            if 'Посл. вход:' in ac.text:
                try:
                    last_login = ac.find("span", {''}).text
                except:
                    last_login = ac.find("span", {'c_red'}).text
                last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)
            elif 'VIP-аккаунт' in ac.text:
                effect = 'VIP'
            elif 'О себе:' in ac.text:
                about = ac.text.split(": ", maxsplit=1)[1].split("\t", maxsplit=1)[0]
            elif 'Премиум-аккаунт' in ac.text:
                effect = 'premium'
            elif 'Семья' in ac.text:
                family_id = int(
                    ac.find("a", {'darkgreen_link'})['href'].split("=")[1])
                family_name = ac.find("a", {'darkgreen_link'}).text
            elif 'Красота' in ac.text:
                beauty = int(ac.text.split(": ")[1])
            elif 'Клуб:' in ac.text:
                club_id = int(ac.find("a", {'class': 'darkgreen_link'})[
                                  'href'].split("=")[1])
                club = ac.text.split(": ")[1].split(",")[0]
                rank_club = ac.text.split(", ")[1]
            elif 'Верность клубу' in ac.text:
                club_const = int(ac.text.split(": ")[1].split("%")[0])
            elif 'Дней в клубе:' in ac.text:
                club_day = ac.text.split(": ")[1].replace('\t', '')
            elif 'Внесено в клуб' in ac.text and club_coin is None:
                club_coin = int(ac.text.split(": ")[1].replace('\t', ''))
            elif 'Внесено в клуб' in ac.text and club_coin:
                club_heart = ac.text.split(": ")[1].replace('\t', '')
            elif 'Дней в игре:' in ac.text:
                day = int(ac.text.split(": ")[1].replace('\t', ''))
        return {'status': 'ok',
                'pet_id': int(pet_id),
                'name': name,
                'ava_id': ava_id,
                'level': int(level),
                'last_login': last_login,
                'about': about,
                'effect': effect,
                'beauty': beauty,
                'family_id': family_id,
                'family_name': family_name,
                'club_id': club_id,
                'club': club,
                'rank': rank_club,
                'club_const': club_const,
                'club_day': club_day,
                'club_coin': club_coin,
                'club_heart': club_heart,
                'day': day}
    except asyncio.TimeoutError as e:
        return {'status': 'error', 'code': '', 'msg': e}
    except Exception as e:
        return {'status': 'error',
                'code': 12,
                'msg': 'Failed to get profile',
                'error': e}


async def view_anketa(pet_id, cookies, timeout, connector):
    try:
        about = real_name = gender = city = birthday = ank = None
        params = {'pet_id': pet_id}
        resp = await requests.get("http://mpets.mobi/view_anketa",
                                  params=params, cookies=cookies)
        prof = BeautifulSoup(await resp.read(), "lxml")
        if "Вы кликаете слишком быстро." in resp.text:
            return await view_anketa(pet_id, cookies, timeout, connector)
        anketa = prof.find_all("span", {"class": "anketa_head ib mb3"})
        for i in range(len(anketa)):
            if "себе" in str(anketa[i].text):
                about = prof.find_all("div", {"class": "mb10"})[i].text
            elif "Реальное имя" in anketa[i].text:
                real_name = prof.find_all("div", {"class": "mb10"})[i].text
            elif "Пол" in anketa[i].text:
                gender = prof.find_all("div", {"class": "mb10"})[i].text
                gender = gender.replace("\r", "").replace("\n", "")
                gender = gender.replace("\t", "")
            elif "Город" in anketa[i].text:
                city = prof.find_all("div", {"class": "mb10"})[i].text
            elif "Дата рождения" in anketa[i].text:
                birthday = prof.find_all("div", {"class": "mb10"})[i].text
            elif "Анкета" in anketa[i].text:
                ank = prof.find_all("div", {"class": "mb10"})[i].text
        return {'status': 'ok',
                'pet_id': int(pet_id),
                'about': about,
                'real_name': real_name,
                'gender': gender,
                'city': city,
                'birthday': birthday,
                'ank': ank}
    except asyncio.TimeoutError as e:
        return await view_anketa(pet_id, cookies, timeout, connector)
    except Exception:
        return {'status': 'error',
                'code': 12,
                'msg': 'Failed to get anketa'}


async def chest(cookies):
    pass


async def view_posters(cookies):
    pass


async def view_gifts(pet_id, page, cookies, timeout, connector):
    try:
        params = {'pet_id': pet_id, "page": page}
        players = []
        resp = await requests.get("http://mpets.mobi/view_gifts",
                                  params=params, cookies=cookies)
        gifts = BeautifulSoup(await resp.read(), "lxml")
        if "Вы кликаете слишком быстро." in resp.text:
            return await view_gifts(pet_id, page, cookies, timeout, connector)
        items = gifts.find_all('div', {'class': 'item'})
        for item in items:
            name, pet_id = None, None
            present_id = item.find("img", {"class": "item_icon"})["src"]
            present_id = present_id.split("present")[1].split(".")[0]
            pet_id = item.find("a", {"class": "pet_name il"})
            if pet_id:
                name = pet_id.text
                pet_id = pet_id["href"].split("=")[1]
            date = item.find("span", {"class": "gray_color font_13"}).text
            date = date.split("получен")[1]
            # НЕ ДЕЛАЙ БЛЯТЬ PET_ID B PRESENT_ID ЧИСЛОВЫМ ТИПОМ

            # 25.06.2021
            # добавили в уп капчу, половину нормального кода приходится переписыать на быструю руку.
            # короче pet_id в принципе можно сделать интовым, но нужна проверка скрытый подарок или нет
            players.append({"pet_id": pet_id, "name": name,
                            "present_id": present_id, "date": date})
        return {'status': 'ok',
                'page': page,
                'players': players}
    except asyncio.TimeoutError as e:
        return {'status': 'error', 'code': '', 'msg': e}
    except Exception as e:
        return {'status': 'error',
                'code': 12,
                'msg': e}


async def post_message(pet_id, message, gift_id, cookies, connector):
    pass
