import random

from sql import crud
from utils.constants import collections


async def check_collected_collection(user_id: int, collection_id: int):
    user_collection = crud.get_user_collection(user_id=user_id,
                                               collection_id=collection_id)
    for counter_types in range(1, 6):
        amount = user_collection.__dict__['type' + str(counter_types)]
        if amount < collections[collection_id]['required'][counter_types - 1]['amount']:
            return False
    return True


async def collect_collection(user_id: int, collection_id: int):
    user_collection = crud.get_user_collection(user_id=user_id,
                                               collection_id=collection_id)
    types = []
    for counter_types in range(1, 6):
        amount = user_collection.__dict__['type' + str(counter_types)]
        types.append(amount - collections[collection_id]['required'][counter_types - 1]['amount'])
    crud.update_user_collection(user_id=user_id,
                                collection_id=collection_id,
                                type1=types[0],
                                type2=types[1],
                                type3=types[2],
                                type4=types[3],
                                type5=types[4])
    return True


async def remove_collection_item(user_id: int, collection_id: int, part_id: int):
    """
    :params user_id: принимает id пользователя
    :params collection_id: принимает id коллекции
    :params part_id: принимает id части из коллекции. (от 1 до 5)
    """
    user_collection = crud.get_user_collection(user_id=user_id,
                                               collection_id=collection_id)
    types = []
    for counter_types in range(1, 6):
        amount = user_collection.__dict__['type' + str(counter_types)]
        if part_id == counter_types:
            types.append(amount - 1)
        else:
            types.append(amount)
    crud.update_user_collection(user_id=user_id,
                                collection_id=collection_id,
                                type1=types[0],
                                type2=types[1],
                                type3=types[2],
                                type4=types[3],
                                type5=types[4])


async def add_collection_item(user_id: int, collection_id: int, part_id: int):
    """
    :params user_id: принимает id пользователя
    :params collection_id: принимает id коллекции
    :params part_id: принимает id части из коллекции. (от 1 до 5)
    """
    user_collection = crud.get_user_collection(user_id=user_id,
                                               collection_id=collection_id)
    types = []
    for counter_types in range(1, 6):
        amount = user_collection.__dict__['type' + str(counter_types)]
        if part_id == counter_types:
            types.append(amount + 1)
        else:
            types.append(amount)
    crud.update_user_collection(user_id=user_id,
                                collection_id=collection_id,
                                type1=types[0],
                                type2=types[1],
                                type3=types[2],
                                type4=types[3],
                                type5=types[4])


async def create_collection_item(user_id: int):
    random_part = random.randint(0, 19)
    part_id, collection_id = 1, 0
    if 0 <= random_part <= 4:
        part_id = random_part + 1
        collection_id = 1
    elif 5 <= random_part <= 9:
        part_id = random_part - 5 + 1
        collection_id = 2
    elif 10 <= random_part <= 14:
        part_id = random_part - 10 + 1
        collection_id = 3
    elif 15 <= random_part <= 19:
        part_id = random_part - 15 + 1
        collection_id = 5
    '''elif 20 <= random_part <= 24:
        part_id = random_part - 20 + 1
        collection_id = 5'''
    '''elif 25 <= random_part <= 29:
        part_id = random_part - 25 + 1
        collection_id = 6'''
    await add_collection_item(user_id=user_id,
                              collection_id=collection_id,
                              part_id=part_id)
    return {"collection_id": collection_id, "part_id": part_id}
