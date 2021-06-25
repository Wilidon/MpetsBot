import random
import string

import aiohttp
from aiohttp import ClientTimeout, ClientSession
import requests_async as requests

from mpetsapi.profile import profile
from mpetsapi.settings import change_pw


async def start(name, password, type, timeout, connector):
    try:
        if name == "standard":
            s = requests.Session()
            await s.get("http://mpets.mobi/start")
            resp = await s.get("http://mpets.mobi/save_gender",
                               params={"type": type})
            # print(resp.text)
            if "Магазин" in resp.text:
                cookies = {"PHPSESSID": s.cookies.values()[0]}
                resp = await profile(cookies, timeout, connector)
                if resp["status"] != "ok":
                    return resp
                return {"status": "ok",
                        "name": resp['name'],
                        "password": password,
                        "cookies": cookies}
    except Exception as e:
        return {"status": "error",
                "code": 1,
                "msg": "Failed to create account"}


import requests_async as requests


async def get_captcha():
    try:

        s = requests.Session()
        r = await s.get('http://mpets.mobi/captcha?r=281')
        cookies = {"PHPSESSID": r.cookies.values()[0]}
        with open("1.jpg", 'wb') as fd:
            fd.write(r.content)
        return {"status": "ok",
                "cookies": cookies}
    except:
        pass


async def login(name, password, captcha, cookies, timeout, connector):
    try:
        r = await requests.post("http://mpets.mobi/login", {"name": name,
                                                            "password": password,
                                                            "captcha": int(captcha)}, cookies=cookies)
        resp = await requests.get("http://mpets.mobi/main", cookies=cookies)
        if "Неверная captcha. " in resp.text:
            return {"status": "error",
                    "code": 1,
                    "msg": "Неверная captcha. Неправильное Имя или Пароль"}
        elif "Неправильное Имя или Пароль" in resp.text:
            return {"status": "error",
                    "code": 2,
                    "msg": "Incorrect name or password"}
        elif "Ваш питомец заблокирован" in resp.text:
            return {"status": "error",
                    "code": 3,
                    "msg": "This account has blocked"}
        elif "Вы кликаете слишком быстро." in resp.text:
            return await login(name, password, timeout, connector)
        elif "Магазин" in resp.text:
            return {"status": "ok",
                    "cookies": cookies}
        else:
            return {"status": "error",
                    "code": 5,
                    "msg": "Authorization failed"}
    except Exception as e:
        return {"status": "error",
                "code": 4,
                "msg": e}
