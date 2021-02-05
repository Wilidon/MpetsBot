from time import time

from sql.database import Session
from . import models
from sqlalchemy import or_

db = Session()


def get_user(user_id: int):
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


def update_club_status(club_id: int, status: str):
    club = db.query(models.Clubs).filter_by(club_id=club_id).first()
    club.status = status
    db.commit()


def get_clubs(status: str):
    return db.query(models.Clubs).filter_by(status=status).all()


def get_users_with_club(club_id: int):
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


def create_chat_message(club_id: int, pet_id: str, message: int, date: int):
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
                          message: str, page: int, post_date: int):
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
        task.status = "timeout"
        db.commit()


def update_user_task(id: int, progress: int, status: str = "waiting"):
    user_task = db.query(models.UsersTasks).filter_by(id=id).first()
    user_task.progress = progress
    user_task.status = status
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
    ban = db.query(models.Bans).filter(models.Bans.user_id == user_id,
                                       models.Bans.ending > ending).first()
    if ban is None:
        ban = models.Bans(user_id=user_id,
                          reason=reason,
                          ending=ending)
        db.add(ban)
        user.access = -1
        db.commit()
        return True
    else:
        return False


def unban(user_id: int):
    ban = db.query(models.Bans).filter(models.Bans.user_id == user_id,
                                       models.Bans.ending > 10).first()
    if ban is None:
        return False
    else:
        ban.ending = 1
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


def get_message(message_id: int):
    return db.query(models.ClubGame).filter_by(message_id=message_id).first()


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
    pet = db.query(models.RacesRatingg).filter_by(place=place).first()
    pet.pet_id = pet_id
    pet.place = place
    pet.score = score
    db.commit()


def get_user_task_name(user_id: int, task_name: str, today: int):
    return db.query(models.UsersTasks).filter_by(user_id=user_id,
                                                 task_name=task_name,
                                                 date=today).first()
