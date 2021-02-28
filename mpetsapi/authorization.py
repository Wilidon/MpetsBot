import random
import string

from aiohttp import ClientTimeout, ClientSession

from mpetsapi.profile import profile
from mpetsapi.settings import change_pw


async def start(name, password, type, timeout, connector):
    try:
        if name == "standard":
            async with ClientSession(timeout=ClientTimeout(total=timeout),
                                     connector=connector) as session:
                await session.get("http://mpets.mobi/start")
                resp = await session.get("http://mpets.mobi/save_gender",
                                         data={"type": type})
                if "Магазин" in await resp.text():
                    cookies = session.cookie_jar.filter_cookies(
                        "http://mpets.mobi")
                    for key, cookie in cookies.items():
                        if cookie.key == "PHPSESSID":
                            cookies = {"PHPSESSID": cookie.value}
                        if cookie.key == "id":
                            pet_id = cookie.value
                    if password:
                        resp = await change_pw(password, cookies,
                                               timeout, connector)
                    else:
                        password = ("".join(
                            random.sample(string.ascii_lowercase, k=10)))
                        resp = await change_pw(password, cookies,
                                               timeout, connector)
                    if resp["status"] != "ok":
                        return resp
                    resp = await profile(pet_id, cookies, timeout, connector)
                    if resp["status"] != "ok":
                        return resp
                    return {"status": "ok",
                            "pet_id": pet_id,
                            "name": resp['name'],
                            "password": password,
                            "cookies": cookies}
    except Exception as e:
        return {"status": "error",
                "code": 1,
                "msg": "Failed to create account"}


async def login(name, password, timeout, connector):
    try:
        async with ClientSession(timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            async with session.post("http://mpets.mobi/login",
                                    data={"name": name,
                                          "password": password}) as resp:
                if "Неправильное Имя или Пароль" in await resp.text():
                    return {"status": "error",
                            "code": 2,
                            "msg": "Incorrect name or password"}
                elif "Ваш питомец заблокирован" in await resp.text():
                    return {"status": "error",
                            "code": 3,
                            "msg": "This account has blocked"}
                elif "Вы кликаете слишком быстро." in await resp.text():
                    return await login(name, password, timeout, connector)
                elif "Магазин" in await resp.text():
                    cookies = session.cookie_jar.filter_cookies(
                        "http://mpets.mobi")
                    for key, cookie in cookies.items():
                        if cookie.key == "PHPSESSID":
                            cookies = {"PHPSESSID": cookie.value}
                        if cookie.key == "id":
                            pet_id = cookie.value
                    return {"status": "ok",
                            "pet_id": pet_id,
                            "cookies": cookies}
                else:
                    return {"status": "error",
                            "code": 5,
                            "msg": "Authorization failed"}
    except Exception as e:
        return {"status": "error",
                "code": 4,
                "msg": e}
