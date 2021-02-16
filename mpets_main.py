import logging

from loguru import logger
from vkwave.bots import SimpleLongPollBot

from blueprints.admin import admin_router
from blueprints.club_tasks import club_router
from blueprints.holidays import holidays_router
from blueprints.menu import menu_router
from blueprints.register import reg_router
from blueprints.shop import shop_router
from blueprints.user_tasks import user_router
from config import get_settings, logger_config
from middlewares import UserMiddleware

__version__ = "1.6.10"

logging.basicConfig(filename="logs/vk.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

if __name__ == "__main__":
    # Настройка логгера
    logger.configure(**logger_config)
    logger.enable("")
    logger.success("Вк бот запущен.")

    # Получаем настройки проекта
    settings = get_settings()
    bot = SimpleLongPollBot(tokens=settings.token, group_id=settings.group_id)

    # Создаем все таблицы в базе данных
    # Подключен alembic, поэтому строчку не нужна
    # models.Base.metadata.create_all(bind=engine)

    # Подключаем промежуточное ПО
    bot.middleware_manager.add_middleware(UserMiddleware())

    # Подключаем роутеры бота
    bot.dispatcher.add_router(shop_router)
    bot.dispatcher.add_router(reg_router)
    bot.dispatcher.add_router(user_router)
    bot.dispatcher.add_router(club_router)
    bot.dispatcher.add_router(holidays_router)
    bot.dispatcher.add_router(admin_router)

    bot.dispatcher.add_router(menu_router)

    # Запускаем бота
    try:
        bot.run_forever()
    except Exception as e:
        logger.error(f"Бот упал {e}")
