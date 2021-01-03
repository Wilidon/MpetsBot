import typing

import pickledb
from vkwave.bots import BaseMiddleware, BotEvent, MiddlewareResult

from sql import crud


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
        return MiddlewareResult(True)
