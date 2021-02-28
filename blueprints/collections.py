import json

from vkwave.bots import DefaultRouter, SimpleBotEvent, \
    simple_bot_message_handler, PayloadFilter

from keyboards.kb import collection_kb, to_collect
from sql import crud
from utils.collection_handler import check_collected_collection, collect_collection
from utils.constants import collections, numbers

collections_router = DefaultRouter()


@simple_bot_message_handler(collections_router,
                            PayloadFilter({"command": "collection_id=1"}) |
                            PayloadFilter({"command": "collection_id=2"}) |
                            PayloadFilter({"command": "collection_id=3"}) |
                            PayloadFilter({"command": "collection_id=4"}) |
                            PayloadFilter({"command": "collection_id=5"}) |
                            PayloadFilter({"command": "collection_id=6"}))
async def collect_collection_handler(event: SimpleBotEvent):
    user = event["current_user"]
    try:
        collection_id = json.loads(event.object.object.message.payload)["command"].split("=")[1]
        collection_id = int(collection_id)
    except Exception:
        return "Ошибка"
    result = await check_collected_collection(user_id=user.user_id,
                                              collection_id=collection_id)
    if result is True:
        await collect_collection(user_id=user.user_id,
                                 collection_id=collection_id)
        crud.add_collected_collection(user_id=user.user_id,
                                      collection_id=collection_id)
        collection_name = collections[collection_id]['name']
        collection_reward = collections[collection_id]['reward']
        crud.add_user_item(user_id=user.user_id,
                           item_name=f"{collection_name} | {collection_reward}",
                           score=777)
        text = f"Коллекция {collection_name} собрана. Ваша награда: {collection_reward}"
        await collection_kb(user=user, event=event, message=text)
    else:
        return "Не хватает частей для сбора коллекции."


@simple_bot_message_handler(collections_router,
                            PayloadFilter({"command": "collections"}))
async def collections_handler(event: SimpleBotEvent):
    user = event["current_user"]
    text = "🧩Коллекции\n\n"
    counter = 0
    for collection in collections.items():
        collection_id = collection[0]
        user_collection = crud.get_user_collection(user_id=user.user_id,
                                                   collection_id=collection_id)
        colletion_name = collection[1]['name']
        required = collection[1]['required']
        reward = collection[1]['reward']
        text += f"{numbers[counter + 1]} {colletion_name} \n" \
                f"Необходимо: \n"
        for data in required:
            text += f"{data['icon']} (х{data['amount']}) "
        text += f"\nСобрано: "
        counter_types = 1
        for data in required:
            amount = user_collection.__dict__['type' + str(counter_types)]
            text += f"{data['icon']} (х{amount}) "
            counter_types += 1
        text += f"\nНаграда за коллекцию: {reward}\n\n"
        counter += 1
    await collection_kb(user=user, event=event, message=text)


@simple_bot_message_handler(collections_router,
                            PayloadFilter({"command": "to_collect"}))
async def to_collect_handler(event: SimpleBotEvent):
    user = event["current_user"]
    text = "🧩 Выберите коллекцию для сбора и получения награды"
    await to_collect(user=user, event=event, message=text)
