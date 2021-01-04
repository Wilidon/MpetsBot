from sql.database import Session
from . import models

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


def get_clubs_stats(limit: int = 10):
    return db.query(models.ClubStats).order_by(
        models.ClubStats.points.desc()).limit(limit).all()


def get_users_stats(limit: int = 10):
    return db.query(models.UserStats).order_by(
        models.UserStats.points.desc()).limit(limit).all()


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


def get_user_tasks(user_id: int, today: int):
    return db.query(models.UsersTasks).filter_by(user_id=user_id,
                                                 date=today).all()


def get_club_tasks(user_id: int, today: int):
    return db.query(models.ClubsTasks).filter_by(user_id=user_id,
                                                 date=today).all()


def create_club_task_for_user(user_id: int, task_name: str, progress: int,
                              end: int, date: int):
    club_task = models.ClubsTasks(user_id=user_id,
                                  task_name=task_name,
                                  progress=progress,
                                  end=end,
                                  date=date)
    db.add(club_task)
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


def close_all_club_tasks(club_id: int):
    users = get_users_with_club(club_id)
    for user in users:
        club_tasks = db.query(models.ClubsTasks).filter_by(
            user_id=user.user_id,
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


def create_upRank_history(club_id: int, owner_id: int, member_id: int,
                          action: str, date: str):
    history = models.ClubUpRankHistory(club_id=club_id,
                                       owner_id=owner_id,
                                       member_id=member_id,
                                       action=action,
                                       date=date)
    db.add(history)
    db.commit()


def check_upRank_history(owner_id: int, member_id: int, action: str,
                         date: str):
    return db.query(models.ClubUpRankHistory).filter_by(owner_id=owner_id,
                                                        member_id=member_id,
                                                        action=action,
                                                        date=date).first()


def create_acceptPlayer_history(club_id: int, owner_id: int, member_id: int,
                                action: str, date: str):
    history = models.ClubAcceptPlayerHistory(club_id=club_id,
                                             owner_id=owner_id,
                                             member_id=member_id,
                                             action=action,
                                             date=date)
    db.add(history)
    db.commit()


def check_acceptPlayer_history(owner_id: int, member_id: int, action: str,
                               date: str):
    return db.query(models.ClubAcceptPlayerHistory).filter_by(
        owner_id=owner_id,
        member_id=member_id,
        action=action,
        date=date).first()


def create_user_task_for_user(user_id: int, task_name: str, progress: int,
                              end: int, date: int):
    club_task = models.UsersTasks(user_id=user_id,
                                  task_name=task_name,
                                  progress=progress,
                                  end=end,
                                  date=date)
    db.add(club_task)
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


def update_bot(user_id: int, pet_id: int, name: str):
    user_bot = db.query(models.Bots).filter_by(user_id=user_id).first()
    user_bot.pet_id = pet_id
    user_bot.name = name
    db.commit()


def add_user_item(user_id: int, item_name: str, score: int):
    item = models.UserItems(user_id=user_id,
                            item_name=item_name,
                            score=score,
                            status="В процессе")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def add_club_item(club_id: int, item_name: str, score: int):
    item = models.ClubItems(club_id=club_id,
                            item_name=item_name,
                            score=score,
                            status="В процессе")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_user_items():
    return db.query(models.UserItems).filter_by(status="В процессе").all()


def get_club_items():
    return db.query(models.ClubItems).filter_by(status="В процессе").all()


def update_user_item(user_id: int, status: str):
    item = db.query(models.UserItems).filter_by(user_id=user_id).first()
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
