from time import time
from typing import List

from sql.database import Session
from . import models
from sqlalchemy import or_

db = Session()


def get_user(user_id: int) -> models.Users:
    return db.query(models.Users).filter_by(user_id=user_id).first()


def create_user(user_id: int, first_name: str, last_name: str):
    user = models.Users(user_id=user_id,
                        first_name=first_name,
                        last_name=last_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users():
    return db.query(models.Users).filter_by().all()


def get_users_with_status(status: str = "ok"):
    return db.query(models.Users).filter_by(status=status).all()


def update_user_status(user_id: int, status: str):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    user.status = status
    db.commit()


def update_user_data(user_id: int, pet_id: int, name: str, club_id: int):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    user.pet_id = pet_id
    user.name = name
    user.club_id = club_id
    db.commit()


def update_user_profile(user_id: int, name: str, club_id: int):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    user.name = name
    user.club_id = club_id
    db.commit()


def check_pet_name(pet_id: int):
    return db.query(models.Users).filter_by(pet_id=pet_id, status="ok").first()


def get_club(club_id: int):
    return db.query(models.Clubs).filter_by(club_id=club_id).first()


def get_clubs_stats_order_by_points(limit: int = 10):
    return db.query(models.ClubStats).order_by(
        models.ClubStats.points.desc()).limit(limit).all()


def get_clubs_stats_order_by_tasks(limit: int = 10):
    return db.query(models.ClubStats).order_by(
        models.ClubStats.total_tasks.desc()).limit(limit).all()


def get_users_stats_order_by_points(limit: int = 10):
    return db.query(models.UserStats).order_by(
        models.UserStats.points.desc()).limit(limit).all()


def get_users_stats_order_by_tasks(limit: int = 10):
    return db.query(models.UserStats).order_by(
        models.UserStats.personal_tasks.desc()).limit(limit).all()


def create_club(club_id: int, name: str, bot_id: int, bot_name: str,
                bot_password: str):
    club = models.Clubs(club_id=club_id,
                        name=name,
                        bot_id=bot_id,
                        bot_name=bot_name,
                        bot_password=bot_password)
    db.add(club)
    db.commit()


def update_club_bot(club_id: int, bot_id: int, bot_name: str, bot_password: str):
    club = db.query(models.Clubs).filter_by(club_id=club_id).first()
    club.bot_id = bot_id
    club.bot_name = bot_name
    club.bot_password = bot_password
    db.commit()


def update_club_status(club_id: int, status: str):
    club = db.query(models.Clubs).filter_by(club_id=club_id).first()
    club.status = status
    db.commit()


def get_clubs(status: str):
    return db.query(models.Clubs).filter_by(status=status).all()


def get_users_with_club(club_id: int) -> List[models.Users]:
    return db.query(models.Users).filter_by(club_id=club_id).all()


def get_user_task(id: int):
    return db.query(models.UsersTasks).filter_by(id=id).first()


def get_user_tasks(user_id: int, today: int):
    return db.query(models.UsersTasks).filter_by(user_id=user_id,
                                                 date=today).all()


def get_user_tasks_with_status(user_id: int, today: int, status: str):
    return db.query(models.UsersTasks).filter_by(user_id=user_id,
                                                 status=status,
                                                 date=today).all()


def get_club_tasks_with_status(user_id: int, today: int):
    return db.query(
        models.ClubsTasks).filter(or_(models.ClubsTasks.status ==
                                      "completed",
                                      models.ClubsTasks.status == "waiting"),
                                  models.ClubsTasks.user_id == user_id,
                                  models.ClubsTasks.date == today).all()


def get_club_task(id: int):
    return db.query(models.ClubsTasks).filter_by(id=id).first()


def get_club_tasks(user_id: int, today: int, status: str = "waiting"):
    return db.query(models.ClubsTasks).filter_by(user_id=user_id,
                                                 status=status,
                                                 date=today).all()


def get_club_tasks_without_status(user_id: int, today: int):
    return db.query(models.ClubsTasks).filter_by(user_id=user_id,
                                                 date=today).all()


def get_club_tasks_all(today: int, status: str = "waiting"):
    return db.query(models.ClubsTasks).filter_by(status=status,
                                                 date=today).all()


def create_club_task_for_user(user_id: int, task_name: str, progress: int,
                              end: int, date: int, status: str = "waiting"):
    club_task = models.ClubsTasks(user_id=user_id,
                                  task_name=task_name,
                                  progress=progress,
                                  end=end,
                                  status=status,
                                  date=date)
    db.add(club_task)
    db.commit()


def update_club_task_v2(id: int, task_name: str, progress: int,
                        end: int, date: int):
    club = db.query(models.ClubsTasks).filter_by(id=id).first()
    club.task_name = task_name
    club.progress = progress
    club.end = end
    club.status = "waiting"
    club.date = date
    db.commit()


def update_club_task(id: int, progress: int, status: str = "waiting"):
    club = db.query(models.ClubsTasks).filter_by(id=id).first()
    club.progress = progress
    club.status = status
    db.commit()


def get_chat_message(club_id: int, pet_id: int, message: str, today: int):
    return db.query(models.ClubChat).filter_by(club_id=club_id,
                                               pet_id=pet_id,
                                               message=message,
                                               date=today).first()


def create_chat_message(club_id: int, pet_id: int, message: str, date: int):
    chat_msg = models.ClubChat(club_id=club_id,
                               pet_id=pet_id,
                               message=message,
                               date=date)
    db.add(chat_msg)
    db.commit()


def get_user_stats(user_id: int):
    return db.query(models.UserStats).filter_by(user_id=user_id).first()


def get_club_stats(club_id: int):
    return db.query(models.ClubStats).filter_by(club_id=club_id).first()


def update_user_stats(user_id, points=0, personal_tasks=0, club_tasks=0,
                      club_points=0):
    user = db.query(models.UserStats).filter_by(user_id=user_id).first()
    if user is None:
        user = models.UserStats(user_id=user_id,
                                points=0,
                                personal_tasks=0,
                                club_tasks=0,
                                club_points=0)
        db.add(user)
        db.commit()
        db.refresh(user)
    user.personal_tasks += personal_tasks
    user.points += points
    user.club_tasks += club_tasks
    user.club_points += club_points
    db.commit()


def update_club_stats(club_id, points=0, total_tasks=0):
    club = db.query(models.ClubStats).filter_by(club_id=club_id).first()
    if club is None:
        club = models.ClubStats(club_id=club_id,
                                points=0,
                                total_tasks=0)
        db.add(club)
        db.commit()
        db.refresh(club)
    club.points += points
    club.total_tasks += total_tasks
    db.commit()


def close_all_club_tasks(user_id: int):
    club_tasks = db.query(models.ClubsTasks).filter_by(
        user_id=user_id,
        status="waiting").all()
    for task in club_tasks:
        task.status = "timeout"
        db.commit()


def get_thread_message(thread_id: int):
    return db.query(models.ThreadsMessages).filter_by(
        thread_id=thread_id).first()


def get_thread_messages(thread_id: int):
    return db.query(models.ThreadsMessages).filter_by(
        thread_id=thread_id).all()


def get_last_page_thread(thread_id: int):
    return db.query(models.ThreadsMessages).filter_by(
        thread_id=thread_id).order_by(
        models.ThreadsMessages.page.desc()).first()


def create_thread_message(club_id: int, pet_id: int, thread_id: int,
                          message: str, page: int, post_date: str):
    thread_msg = models.ThreadsMessages(club_id=club_id,
                                        pet_id=pet_id,
                                        thread_id=thread_id,
                                        message=message,
                                        page=page,
                                        post_date=post_date)
    db.add(thread_msg)
    db.commit()


def check_msg(thread_id: int, message: str, post_date: str, page: int):
    return db.query(models.ThreadsMessages).filter_by(thread_id=thread_id,
                                                      message=message,
                                                      post_date=post_date,
                                                      page=page).first()


def create_user_task_for_user(user_id: int, task_name: str, progress: int,
                              end: int, date: int):
    user_task = models.UsersTasks(user_id=user_id,
                                  task_name=task_name,
                                  progress=progress,
                                  end=end,
                                  date=date)
    db.add(user_task)
    db.commit()


def close_all_user_tasks(user_id: int):
    user_tasks = db.query(models.UsersTasks).filter_by(
        user_id=user_id,
        status="waiting").all()
    for task in user_tasks:
        if task.date == 214:
            continue
        if task.date == 223:
            continue
        if task.date == 308:
            continue
        if task.date == 401:
            continue
        if task.date == 501:
            continue
        task.status = "timeout"
        db.commit()


def close_all_user_htasks(user_id: int, date: int):
    user_tasks = db.query(models.UsersTasks).filter_by(
        user_id=user_id,
        status="waiting").all()
    for task in user_tasks:
        if task.date == date:
            task.status = "timeout"
        db.commit()


def update_user_task(id: int, progress: int, status: str = "waiting"):
    user_task = db.query(models.UsersTasks).filter_by(id=id).first()
    user_task.progress = progress
    user_task.status = status
    db.commit()


def update_user_task_end(id: int, end: int):
    user_task = db.query(models.UsersTasks).filter_by(id=id).first()
    user_task.end = end
    db.commit()


def update_user_task_name(id: int, task_name: str):
    user_task = db.query(models.UsersTasks).filter_by(id=id).first()
    user_task.task_name = task_name
    db.commit()


def reset_task(user_id: int):
    user_task = db.query(models.UsersTasks).filter_by(user_id=user_id,
                                                      status='waiting').all()
    for t in user_task:
        t.date = 1
    db.commit()


def reset_club_task(user_id: int):
    user_task = db.query(models.ClubsTasks).filter_by(user_id=user_id,
                                                      status='waiting').all()
    for t in user_task:
        t.date = 1
    db.commit()


def create_bot(user_id: int, pet_id: int, name: str, password: str):
    bot = models.Bots(user_id=user_id,
                      pet_id=pet_id,
                      name=name,
                      password=password)
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


def get_bot(user_id: int):
    return db.query(models.Bots).filter_by(user_id=user_id).first()


def update_bot(user_id: int, pet_id: int, name: str, password: str):
    user_bot = db.query(models.Bots).filter_by(user_id=user_id).first()
    user_bot.pet_id = pet_id
    user_bot.name = name
    user_bot.password = password
    db.commit()


def add_user_item(user_id: int, item_name: str, score: int,
                  status: str = "В процессе"):
    item = models.UserItems(user_id=user_id,
                            item_name=item_name,
                            score=score,
                            status=status)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def add_club_item(club_id: int, item_name: str, score: int,
                  status: str = "В процессе"):
    item = models.ClubItems(club_id=club_id,
                            item_name=item_name,
                            score=score,
                            status=status)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_user_item(user_id: int, status="В процессе"):
    return db.query(models.UserItems).filter(
        models.UserItems.user_id == user_id,
        models.UserItems.status.like(status)).order_by(
        models.UserItems.id.asc()).all()


def get_user_items():
    return db.query(models.UserItems).filter_by(status="В процессе").all()


def get_all_user_items():
    return db.query(models.UserItems).all()


def get_user_items_with_score(score: int):
    return db.query(models.UserItems).filter_by(score=score,
                                                status="В процессе").all()


def get_club_items():
    return db.query(models.ClubItems).filter_by(status="В процессе").all()


def get_all_club_items():
    return db.query(models.ClubItems).all()


def get_club_items_with_score(score: int):
    return db.query(models.ClubItems).filter_by(score=score,
                                                status="В процессе").all()


def update_user_item(user_id: int, status: str):
    item = db.query(models.UserItems).filter_by(user_id=user_id).first()
    item.status = status
    db.commit()


def update_user_itemname(id: int, name: str, status: str):
    item = db.query(models.UserItems).filter_by(id=id).first()
    item.item_name = name
    item.status = status
    db.commit()


def update_club_item(user_id: int, status: str):
    item = db.query(models.ClubItems).filter_by(user_id=user_id).first()
    item.status = status
    db.commit()


def get_amount_users():
    return db.query(models.Users).count()


def get_personal_tasks():
    return db.query(models.UsersTasks).count()


def get_personal_tasks_with_filter(status: str = "waiting"):
    return db.query(models.UsersTasks).filter_by(status=status).count()


def get_amount_clubs():
    return db.query(models.Clubs).count()


def get_clubs_tasks():
    return db.query(models.ClubsTasks).count()


def get_clubs_tasks_with_filter(status: str = "waiting"):
    return db.query(models.ClubsTasks).filter_by(status=status).count()


def reset_user_stats(user_id: int):
    stats = db.query(models.UserStats).filter_by(user_id=user_id).first()
    stats.club_tasks = 0
    stats.club_points = 0
    db.commit()


def confirm_user_item(item_id: int):
    if db.query(models.UserItems).filter_by(id=item_id).first():
        item = db.query(models.UserItems).filter_by(id=item_id).first()
        item.status = "completed"
        db.commit()
        return True
    else:
        return False


def confirm_club_item(item_id: int):
    if db.query(models.ClubItems).filter_by(id=item_id).first():
        item = db.query(models.ClubItems).filter_by(id=item_id).first()
        item.status = "completed"
        db.commit()
        return True
    else:
        return False


def create_user_log(user_id: int, task_name: int, points: int,
                    tasks: int, date: int):
    log = models.UserTaskLog(user_id=user_id,
                             task_name=task_name,
                             points=points,
                             tasks=tasks,
                             date=date)
    db.add(log)
    db.commit()


def create_club_log(user_id: int, task_name: int, club_id: int,
                    points: int, tasks: int, date: int):
    log = models.ClubTaskLog(user_id=user_id,
                             task_name=task_name,
                             club_id=club_id,
                             points=points,
                             tasks=tasks,
                             date=date)
    db.add(log)
    db.commit()


def wipe():
    users_stats = get_users_stats_order_by_tasks(limit=None)
    for user in users_stats:
        user = db.query(models.UserStats).filter_by(
            user_id=user.user_id).first()
        user.points = 0
    clubs_stats = get_clubs_stats_order_by_points(limit=None)
    for club in clubs_stats:
        club = db.query(models.ClubStats).filter_by(
            club_id=club.club_id).first()
        club.points = 0
    db.commit()
    return True


def ban(user_id: int, reason: str, ending: int):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    ban_info = db.query(models.Bans).filter(models.Bans.user_id == user_id,
                                            models.Bans.ending > ending).first()
    if ban_info is None:
        ban_info = models.Bans(user_id=user_id,
                               reason=reason,
                               ending=ending)
        db.add(ban_info)
        user.access = -1
        db.commit()
        return True
    else:
        return False


def unban(user_id: int):
    ban_info = db.query(models.Bans).filter(models.Bans.user_id == user_id,
                                            models.Bans.ending > 10).first()
    if ban_info is None:
        return False
    else:
        ban_info.ending = 1
        db.commit()
        return True


def get_ban(user_id: int):
    return db.query(models.Bans).filter(models.Bans.user_id == user_id,
                                        models.Bans.ending > 10).first()


def update_user_access(user_id: int, access: int):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    user.access = access
    db.commit()
    return True


def get_message(thread_id: int, message_id: int):
    return db.query(models.ClubGame).filter_by(thread_id=thread_id,
                                               message_id=message_id).first()


def get_user_pet_id(pet_id: int):
    return db.query(models.Users).filter_by(pet_id=pet_id).first()


def create_play_message(pet_id: int, thread_id: int, message_id: int, page: int):
    play_msg = models.ClubGame(pet_id=pet_id,
                               thread_id=thread_id,
                               message_id=message_id,
                               page=page)
    db.add(play_msg)
    db.commit()


def get_charm_rating(pet_id: int):
    return db.query(models.CharmRating).filter_by(pet_id=pet_id).first()


def get_races_rating(pet_id: int):
    return db.query(models.RacesRating).filter_by(pet_id=pet_id).first()


def get_charm_place(place: int):
    return db.query(models.CharmRating).filter_by(place=place).first()


def get_races_place(place: int):
    return db.query(models.RacesRating).filter_by(place=place).first()


def create_charm_rating(pet_id: int, place: int, score: int):
    top = models.CharmRating(pet_id=pet_id,
                             place=place,
                             score=score)
    db.add(top)
    db.commit()


def create_races_rating(pet_id: int, place: int, score: int):
    top = models.RacesRating(pet_id=pet_id,
                             place=place,
                             score=score)
    db.add(top)
    db.commit()


def update_charm_rating(pet_id: int, place: int, score: int):
    pet = db.query(models.CharmRating).filter_by(pet_id=pet_id).first()
    pet.place = place
    pet.score = score
    db.commit()


def update_races_rating(pet_id: int, place: int, score: int):
    pet = db.query(models.RacesRating).filter_by(pet_id=pet_id).first()
    pet.place = place
    pet.score = score
    db.commit()


def update_charm_place(pet_id: int, place: int, score: int):
    pet = db.query(models.CharmRating).filter_by(place=place).first()
    pet.pet_id = pet_id
    pet.place = place
    pet.score = score
    db.commit()


def update_races_place(pet_id: int, place: int, score: int):
    pet = db.query(models.RacesRating).filter_by(place=place).first()
    pet.pet_id = pet_id
    pet.place = place
    pet.score = score
    db.commit()


def get_user_task_name(user_id: int, task_name: str, today: int):
    return db.query(models.UsersTasks).filter_by(user_id=user_id,
                                                 task_name=task_name,
                                                 date=today).first()


def create_gift_pair(pet_id: int, friend_id: int, present_id: int, date: int):
    pair = models.ExchangeGifts(pet_id=pet_id,
                                friend_id=friend_id,
                                present_id=present_id,
                                date=date)
    db.add(pair)
    db.commit()


def get_all_pairs(pet_id: int):
    return db.query(models.ExchangeGifts).filter_by(pet_id=pet_id).all()


def get_pet_pair(pet_id: int, friend_id: int, date: int):
    return db.query(models.ExchangeGifts).filter_by(pet_id=pet_id,
                                                    friend_id=friend_id,
                                                    date=date).first()


def open_all_user_htasks(date: int):
    user_tasks = db.query(models.UsersTasks).filter_by(
        status="waiting").all()
    for task in user_tasks:
        if task.date == date:
            task.status = "waiting"
        db.commit()


def get_user_collection(user_id: int, collection_id: int):
    user_collection = db.query(models.Collections).filter_by(user_id=user_id,
                                                             collection_id=collection_id).first()
    if user_collection is None:
        user_collection = models.Collections(user_id=user_id,
                                             collection_id=collection_id)
        db.add(user_collection)
        db.commit()
        db.refresh(user_collection)
    return user_collection


def update_user_collection(user_id: int, collection_id: int, type1: int,
                           type2: int, type3: int, type4: int, type5: int):
    user_collection = db.query(models.Collections).filter_by(user_id=user_id,
                                                             collection_id=collection_id).first()
    user_collection.type1 = type1
    user_collection.type2 = type2
    user_collection.type3 = type3
    user_collection.type4 = type4
    user_collection.type5 = type5
    db.commit()


def add_collected_collection(user_id: int, collection_id: int):
    user_collection = models.CollectedCollections(user_id=user_id,
                                                  collection_id=collection_id)
    db.add(user_collection)
    db.commit()


def create_collection_log(user_id: int, part_id: int, collection_id: int):
    user_collection = models.CollectionsLog(user_id=user_id,
                                            part_id=part_id,
                                            collection_id=collection_id)
    db.add(user_collection)
    db.commit()


def get_user_task_log(user_id: int, limit: int = 3):
    return db.query(models.UserTaskLog).filter_by(user_id=user_id).order_by(
        models.UserTaskLog.id.desc()).limit(limit=limit).all()


def get_club_task_log(user_id: int, limit: int = 3):
    return db.query(models.ClubTaskLog).filter_by(user_id=user_id).order_by(
        models.ClubTaskLog.id.desc()).limit(limit=limit).all()


def get_collection_log(user_id: int, limit: int = 3):
    return db.query(models.CollectionsLog).filter_by(user_id=user_id).order_by(
        models.CollectionsLog.id.desc()).limit(limit=limit).all()


def total_wipe():
    users_stats = get_users_stats_order_by_tasks(limit=None)
    for user in users_stats:
        user = db.query(models.UserStats).filter_by(
            user_id=user.user_id).first()
        user.points = 0
        user.personal_tasks = 0
    clubs_stats = get_clubs_stats_order_by_points(limit=None)
    for club in clubs_stats:
        club = db.query(models.ClubStats).filter_by(
            club_id=club.club_id).first()
        club.points = 0
        club.total_tasks = 0
    db.commit()
    return True


def mega_total_wipe():
    users_stats = get_users_stats_order_by_tasks(limit=None)
    for user in users_stats:
        user = db.query(models.UserStats).filter_by(
            user_id=user.user_id).first()
        user.club_tasks = 0
        user.club_points = 0
    db.commit()
    return True


def total_plus(user_id, tasks, points):
    user = db.query(models.UserStats).filter_by(
        user_id=user_id).first()
    user.points = points
    user.personal_tasks = tasks
    db.commit()
    return True


def total_c_plus(club_id, tasks, points):
    club = db.query(models.ClubStats).filter_by(
        club_id=club_id).first()
    club.points = points
    club.total_tasks = tasks
    db.commit()
    return True


def get_name(name):
    return db.query(models.Users).filter_by(name=name).first()


def get_club_name(name):
    return db.query(models.Clubs).filter_by(name=name).first()


def get_tasks_with_date(date: int):
    return db.query(models.UsersTasks).filter_by(date=date).all()


def delete_colletion_6():
    return db.query(models.Collections).filter_by(collection_id=6).all()


def get_current_boss():
    return db.query(models.Boss).order_by(
        models.Boss.id.desc()).first()


def create_boss(boss_id: int, health_points: int):
    boss = models.Boss(boss_id=boss_id,
                       health_points=health_points)
    db.add(boss)
    db.commit()


def create_damage_log(user_id: int, boss_id: int, damage: int):
    boss_damage = models.BossDamage(user_id=user_id,
                                    boss_id=boss_id,
                                    damage=damage)
    db.add(boss_damage)
    db.commit()


def update_boss_health(boss_id: int, damage: int):
    boss = db.query(models.Boss).filter_by(id=boss_id).first()
    boss.health_points -= damage
    db.commit()
    db.refresh(boss)
    return boss


def update_boss_status(boss_id: int, status: str):
    boss = db.query(models.Boss).filter_by(id=boss_id).first()
    boss.status = status
    db.commit()
    db.refresh(boss)
    return boss


def update_user_boss_reward(user_id: int, boss_id: int, reward: str):
    boss = db.query(models.BossRewards).filter_by(user_id=user_id,
                                                  boss_id=boss_id).first()
    boss.reward = reward
    db.commit()
    db.refresh(boss)
    return boss


def get_users_boss_reward(boss_id: int):
    return db.query(models.BossRewards).filter_by(boss_id=boss_id).order_by(
        models.BossRewards.total_damage.desc()).all()


def update_boss_reward(user_id: int, boss_id: int, damage: int = 0):
    boss_reward = db.query(models.BossRewards).filter_by(user_id=user_id,
                                                         boss_id=boss_id).first()
    if boss_reward is None:
        boss_reward = models.BossRewards(user_id=user_id,
                                         boss_id=boss_id)
        db.add(boss_reward)
        db.commit()
        db.refresh(boss_reward)
    boss_reward.total_damage += damage
    db.commit()
    db.refresh(boss_reward)
    return boss_reward


def update_boss_reward_status(user_id: int, boss_id: int, status: str = 'killed'):
    boss_reward = db.query(models.BossRewards).filter_by(user_id=user_id,
                                                         boss_id=boss_id).first()
    if boss_reward is None:
        boss_reward = models.BossRewards(user_id=user_id,
                                         boss_id=boss_id,
                                         status=status)
        db.add(boss_reward)
        db.commit()
        db.refresh(boss_reward)
    boss_reward.status = status
    db.commit()
    db.refresh(boss_reward)
    return boss_reward


def get_user_killed_boss(boss_id: int, status: str = 'killed'):
    return db.query(models.BossRewards).filter_by(boss_id=boss_id,
                                                  status=status).first()


def get_user_boss(user_id: int, boss_id: int):
    return db.query(models.BossRewards).filter_by(user_id=user_id,
                                                  boss_id=boss_id).first()


def get_user_with_max_damage(boss_id: int):
    return db.query(models.BossRewards).filter_by(boss_id=boss_id).order_by(
        models.BossRewards.total_damage.desc()).first()


def update_boss_restart(user_id: int, amount: int):
    boss = db.query(models.BossRestart).filter_by(user_id=user_id).first()
    if boss is None:
        boss = models.BossRestart(user_id=user_id,
                                  amount=0,
                                  time=int(time()))
        db.add(boss)
        db.commit()
        db.refresh(boss)
    boss.amount = amount
    db.commit()
    db.refresh(boss)
    return boss


def update_boss_restart_time(user_id: int, time: int):
    boss = db.query(models.BossRestart).filter_by(user_id=user_id).first()
    if boss is None:
        boss = models.BossRestart(user_id=user_id,
                                  amount=0,
                                  time=int(time()))
        db.add(boss)
        db.commit()
        db.refresh(boss)
    boss.time = time
    db.commit()
    db.refresh(boss)
    return boss


def get_user_restart(user_id: int):
    boss = db.query(models.BossRestart).filter_by(user_id=user_id).first()
    if boss is None:
        boss = models.BossRestart(user_id=user_id,
                                  amount=0,
                                  time=int(time()))
        db.add(boss)
        db.commit()
        db.refresh(boss)
    return boss


def restart_user_time():
    users = db.query(models.BossRestart).all()
    for user in users:
        user.amount = 0
        user.time = 0
    db.commit()


def health(userinfo: int = False, usertasks: int = False, clubtasks: int = False,
           charm: int = False, races: int = False, time: int = False):
    health_record = db.query(models.Health).first()
    if health_record is None:
        health_record = models.Health()
        db.add(health_record)
        db.commit()
    if userinfo is not False:
        health_record.userinfo = userinfo
    if usertasks is not False:
        health_record.usertasks = usertasks
    if clubtasks is not False:
        health_record.clubtasks = clubtasks
    if charm is not False:
        health_record.charm = charm
    if races is not False:
        health_record.races = races
    if time is not False:
        health_record.time = time
    db.commit()
    db.refresh(health_record)
    return health_record


def get_boss_stats(boss_id: int):
    return db.query(models.BossDamage).filter_by(boss_id=boss_id).order_by(
        models.BossDamage.id.asc()).all()


def change_pet_id(user_id: int, to_user_id: int):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    user2 = db.query(models.Users).filter_by(user_id=to_user_id).first()


def add_rewards(user_id: int, points: int = 0, personal_tasks: int = 0,
                club_points: int = 0, club_tasks: int = 0):
    if points != 0:
        user = db.query(models.UserStats).filter_by(user_id=user_id).first()
        user.points += points
    if personal_tasks != 0:
        user = db.query(models.UserStats).filter_by(user_id=user_id).first()
        user.personal_tasks += personal_tasks
    if club_points != 0:
        user = db.query(models.Users).filter_by(user_id=user_id).first()
        if user.club_id != 0:
            club = db.query(models.ClubStats).filter_by(club_id=user.club_id).first()
            if club is None:
                pass
            club.points += club_points
    if club_tasks != 0:
        user = db.query(models.Users).filter_by(user_id=user_id).first()
        if user.club_id != 0:
            club = db.query(models.ClubStats).filter_by(club_id=user.club_id).first()
            if club is None:
                pass
            club.total_tasks += club_tasks
    db.commit()
    return True