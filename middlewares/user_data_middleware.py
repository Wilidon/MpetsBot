import datetime
import time
import typing
from random import randint

import pickledb
from vkwave.bots import BaseMiddleware, BotEvent, MiddlewareResult

from sql import crud
from utils.constants import month


class UserMiddleware(BaseMiddleware):
    async def pre_process_event(self, event: BotEvent) -> MiddlewareResult:

        db = pickledb.load("./stats.db", True)
        stats = db.get('total_clicks')
        db.set('total_clicks', stats+1)

        user_id = event.object.object.message.from_id

        user = crud.get_user(user_id)
        user_stats = crud.update_user_stats(user_id)
        if user_stats and user.club_id != 0:
            crud.update_club_stats(user.club_id)
        if user is None:
            user_data = await event.api_ctx.users.get(user_ids=user_id)
            user = crud.create_user(user_data.response[0].id,
                                    user_data.response[0].first_name,
                                    user_data.response[0].last_name)
        event["current_user"] = user
        if user.access == -1:
            ban = crud.get_ban(user_id)
            if ban.ending < time.time() + 10800:
                crud.update_user_access(user_id, 1)
                crud.unban(user_id)
                return MiddlewareResult(True)
            d = datetime.datetime.utcfromtimestamp(
                ban.ending).strftime('%d')
            m = datetime.datetime.utcfromtimestamp(
                ban.ending).strftime('%m')
            h = datetime.datetime.utcfromtimestamp(
                ban.ending).strftime('%H:%M')
            left_time = f"{d} {month[m]} в {h}"
            await event.api_ctx.messages.send(user_id=user_id,
                                              message=f"Вы забанены.\n"
                                                      f"Причина: "
                                                      f"{ban.reason}\n"
                                                      f"Окончание бана:"
                                                      f" {left_time}",
                                              random_id=randint(1, 99999999))
            return MiddlewareResult(False)
        if user.access > 0:
            return MiddlewareResult(True)
        today = int(datetime.datetime.today().strftime("%Y%m%d"))
        if today == 20210228:
            await event.api_ctx.messages.send(user_id=user_id,
                                              message=f"Идет подготовка к новому сезону.\n"
                                                      f"Бот будет доступен в 0:00 по МСК!",
                                              random_id=randint(1, 99999999))
            return MiddlewareResult(False)
        return MiddlewareResult(True)
