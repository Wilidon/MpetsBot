import asyncio
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def actions(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            for a in range(3):
                for b in range(5):
                    await session.get("http://mpets.mobi/",
                                      params={"action": "food", "rand": 1})
                    await asyncio.sleep(0.4)
                    await session.get("http://mpets.mobi/",
                                      params={"action": "play", "rand": 1})
                    await asyncio.sleep(0.4)
                    while True:
                        r = await session.get("https://mpets.mobi/show")
                        await asyncio.sleep(0.4)
                        if "Соревноваться" in await r.text():
                            await session.get("https://mpets.mobi/show")
                            await asyncio.sleep(0.4)
                        else:
                            break
                await wakeup(cookies, timeout, connector)
            await session.close()
        return {"status": "ok"}
    except Exception as e:
        return {'status': 'error', 'code': 5, 'msg': 'Failed'}


def action_food(cookies):
    pass


def action_play(cookies):
    pass


def show(cookies):
    pass


async def wakeup_sleep_info(cookies):
    pass


def wakeup_sleep(cookies):
    pass


async def wakeup(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            await session.get("http://mpets.mobi/wakeup")
            await session.close()
            return {'status': 'ok'}
    except:
        return {"status": "error"}


async def charm(cookies, connector):
    pass


async def charm_in_queue(cookies, connector):
    pass


async def charm_out_queue(cookies, connector):
    pass


async def charm_attack(cookies, coonnector):
    pass


async def charm_change(cookies, connector):
    pass


async def charm_dodge(cookies, connector):
    pass


async def races(cookies, connector):
    pass


async def races_in_queue(cookies, connector):
    pass


async def races_out_queue(cookies, connector):
    pass


async def races_go(cookies, connector):
    pass


async def races_attack(cookies, connector):
    pass


async def races_change(cookies, connector):
    pass


async def glade(cookies, connector):
    pass


async def glade_dig(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            await session.get("http://mpets.mobi/glade_dig")
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def travel(cookies, timeout, connector):
    pass


async def go_travel(travel_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            await session.get("http://mpets.mobi/go_travel",
                              data={"travel_id": travel_id})
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def train(cookies, connector):
    pass


async def train_skill(skill, cookies, connector):
    pass


async def assistants(cookies, connector):
    pass


async def assistants_train(type, cookies, connector):
    pass


async def jewels(cookies, connector):
    pass


async def collect_jewel(jewel_id, cookies, connector):
    pass


async def home(cookies, connector):
    pass


async def garden(cookies, connector):
    pass


async def garden_collect(garden_id, cookies, connector):
    pass


async def task(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            r = await session.get("http://mpets.mobi/task")
            r = BeautifulSoup(await r.read(), 'lxml')
            tasks = r.find_all('div', {'class': 'msg mrg_msg2 mt32'})
            for task in tasks:
                if "Забрать награду" in task.text:
                    task_id = \
                    task.find('div', {'class': 'span3'}).next_element.next_element[
                        'href']
                    await session.get("http://mpets.mobi" + str(task_id))
            await session.close()
    except:
        pass


async def task_reward(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            r = await session.get("http://mpets.mobi/task")
            r = BeautifulSoup(await r.read(), 'lxml')
            tasks = r.find_all('div', {'class': 'msg mrg_msg2 mt32'})
            for task in tasks:
                if "Забрать награду" in task.text:
                    task_id = \
                        task.find('div', {
                            'class': 'span3'}).next_element.next_element[
                            'href']
                    await session.get("http://mpets.mobi" + str(task_id))
            await session.close()
    except:
        pass


async def items(category, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"category": category}
            if category == "home":
                pass
            elif category == "effect":
                resp = await session.get("http://mpets.mobi/items",
                                       params=params)
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await items(category, cookies, timeout, connector)
                resp = BeautifulSoup(await resp.read(), "lxml")
                effects = resp.find_all("div", {"class": "shop_item"})
                if len(effects) == 1:
                    if "VIP-аккаунт" in effects[0]:
                        if "Осталось" in effects[0]:
                            left_time = \
                            effects[0].find('div', {'class': 'succes '
                                                      'mt3'}).text.split(
                                "Осталось: ")[1]
                            return {"status": "ok",
                                    "effect": "VIP",
                                    "left_time": left_time}
                        return {"status": "ok",
                                "effect": "None"}
                elif len(effects) == 2:
                    for effect in effects:
                        if "Премиум-аккаунт" in effect:
                            if "Осталось" in effect:
                                left_time = effect.find('div', {
                                    'class': 'succes mt3'}).text.split(
                                    "Осталось: ")[1]
                                return {"status": "ok",
                                        "effect": "premium",
                                        "left_time": left_time}
                        if "VIP-аккаунт" in effect:
                            return {"status": "ok",
                                    "effect": "None"}
            elif category == "food":
                pass
            elif category == "play":
                pass

    except:
        pass


async def buy(category, item_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"category": category, "id": item_id}
            if category == "home":
                pass
            elif category == "effect":
                resp = await session.get("http://mpets.mobi/buy",
                                         params=params)
                return {"status": "ok"}
            elif category == "food":
                pass
            elif category == "play":
                pass
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def best(type, page, cookies, timeout, connector):
    try:
        def has_class(tag):
            return not tag.has_attr("class")

        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {type: "true", "page": page}
            pets = []
            resp = await session.get("http://mpets.mobi/best", params=params)
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await best(type, page, cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("table", {"class": "players tlist font_14 td_un"})
            resp = resp.find_all(has_class, recursive=False)
            for pet in resp:
                place = int(pet.find("td").text)
                pet_id = pet.find("a", {"class": "c_brown3"})['href']
                pet_id = int(pet_id.split("id=")[1])
                name = pet.find("a", {"class": "c_brown3"}).text
                beauty = int(pet.find_all("td")[2].text)
                pets.append({"place": place,
                             "pet_id": pet_id,
                             "name": name,
                             "score": beauty})
            return {"status": "ok",
                    "pets": pets}
    except Exception as e:
        return {"status": "error",
                "code": 0,
                "msg": e}


async def find_pet(name, cookies, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            data, account_status = {'name': name}, None
            resp = await session.post("http://mpets.mobi/find_pet", data=data)
            if "Имя должно быть от 3 до 12 символов!" in await resp.text():
                return {'status': 'error', 'code': 0, 'msg': ''}
            elif "Питомец не найден!" in await resp.text():
                return {'status': 'error', 'code': 0, 'msg': ''}
            elif "Игрок заблокирован" in await resp.text():
                account_status = 'block'
            elif "Игрок забанен" in await resp.text():
                account_status = 'ban'
            elif "view_profile" in str(resp.url):
                pet_id = str(resp.url).split("id=")[1].split("&")[0]
            await session.close()
            return {'status': 'ok',
                    'pet_id': pet_id,
                    'name': name,
                    'account_status': account_status}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def show_coin(cookies, connector):
    pass


async def show_coin_get(cookies, connector):
    pass


async def online(cookies, connector):
    pass


async def game_time(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            resp = await session.get("http://mpets.mobi/main")
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await game_time(cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div", {"class": "small mt20 mb20 c_lbrown cntr td_un"})
            time = resp.find("div", {"class": "mt5 mb5"}).text.split(", ")[1].split("\n")[0]
            return {"status": "ok",
                    "time": time}
    except Exception as e:
        return {"status": "error",
                "code": 0,
                "msg": e}


async def items_effect_vip(cookies, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'category': 'effect', 'id': 2}
            await session.post("http://mpets.mobi/buy", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}
