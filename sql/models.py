import time

import pytz
from sqlalchemy import (Column, Integer, String,
                        BigInteger, SmallInteger, func, DateTime)

from .database import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    first_name = Column(String(64))
    last_name = Column(String(64))
    pet_id = Column(Integer, default=0)
    name = Column(String(32), default=0)
    club_id = Column(Integer, default=0)
    access = Column(SmallInteger, default=0)
    status = Column(String, default="newbie")
    created_at = Column(Integer, default=time.time())


class Bots(Base):
    __tablename__ = "bots"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    pet_id = Column(Integer)
    name = Column(String(32))
    password = Column(String(32))


class UsersTasks(Base):
    __tablename__ = "userstasks"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    task_name = Column(String)
    progress = Column(BigInteger)
    end = Column(BigInteger)
    status = Column(String, default="waiting")
    date = Column(Integer)


class UserStats(Base):
    __tablename__ = "userstats"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    points = Column(Integer)
    personal_tasks = Column(Integer)
    club_tasks = Column(Integer)
    club_points = Column(Integer)


class Clubs(Base):
    __tablename__ = "clubs"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    name = Column(String)
    bot_id = Column(Integer)
    bot_name = Column(String(32))
    bot_password = Column(String(32))
    score = Column(Integer, default=0)
    status = Column(String, default="waiting")


class ClubsTasks(Base):
    __tablename__ = "clubstasks"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    task_name = Column(String)
    progress = Column(BigInteger)
    end = Column(BigInteger)
    status = Column(String, default="waiting")
    date = Column(Integer)


class ClubStats(Base):
    __tablename__ = "clubstats"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    points = Column(Integer)
    total_tasks = Column(Integer)


class ClubChat(Base):
    __tablename__ = "clubchat"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    pet_id = Column(Integer)
    message = Column(String)
    date = Column(Integer)


class ThreadsMessages(Base):
    __tablename__ = "threadsmessages"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    pet_id = Column(Integer)
    thread_id = Column(Integer)
    message = Column(String)
    page = Column(Integer)
    post_date = Column(String)


class UserItems(Base):
    __tablename__ = "useritems"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    item_name = Column(String)
    score = Column(Integer)
    status = Column(String, default="Ожидает")


class ClubItems(Base):
    __tablename__ = "clubitems"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(BigInteger)
    item_name = Column(String)
    score = Column(Integer)
    status = Column(String, default="Ожидает")


class UserTaskLog(Base):
    __tablename__ = "usertasklog"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    task_name = Column(String)
    points = Column(SmallInteger)
    tasks = Column(SmallInteger)
    date = Column(Integer)


class ClubTaskLog(Base):
    __tablename__ = "clubtasklog"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    task_name = Column(String)
    club_id = Column(Integer)
    points = Column(SmallInteger)
    tasks = Column(SmallInteger)
    date = Column(Integer)


class ClubGame(Base):
    __tablename__ = "clubgame"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pet_id = Column(Integer)
    thread_id = Column(Integer)
    message_id = Column(Integer)
    page = Column(Integer)


class CharmRating(Base):
    __tablename__ = "charmrating"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pet_id = Column(Integer)
    place = Column(Integer)
    score = Column(Integer)


class RacesRating(Base):
    __tablename__ = "racesrating"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pet_id = Column(Integer)
    place = Column(Integer)
    score = Column(Integer)


class ExchangeGifts(Base):
    __tablename__ = "exchangegifts"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pet_id = Column(Integer)
    friend_id = Column(Integer)
    present_id = Column(Integer)
    date = Column(Integer, default=None)


class Collections(Base):
    __tablename__ = "collections"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    collection_id = Column(Integer)
    type1 = Column(Integer, default=0)
    type2 = Column(Integer, default=0)
    type3 = Column(Integer, default=0)
    type4 = Column(Integer, default=0)
    type5 = Column(Integer, default=0)


class CollectedCollections(Base):
    __tablename__ = "collectedcollections"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    collection_id = Column(Integer)
    collected_time = Column(DateTime(timezone=True), default=func.now(tz=pytz.timezone('Etc/GMT+3')))


class CollectionsLog(Base):
    __tablename__ = "collectionslog"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    part_id = Column(Integer)
    collection_id = Column(Integer)
    collected_time = Column(DateTime(timezone=True), default=func.now(tz=pytz.timezone('Etc/GMT+3')))


class Boss(Base):
    __tablename__ = "boss"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    boss_id = Column(Integer)
    health_points = Column(Integer)
    status = Column(String, default="ok")
    created_at = Column(DateTime(timezone=True), default=func.now(tz=pytz.timezone('Etc/GMT+3')))


class BossDamage(Base):
    __tablename__ = "damageboss"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    boss_id = Column(Integer)
    damage = Column(Integer)
    damage_time = Column(DateTime(timezone=True), default=func.now(tz=pytz.timezone('Etc/GMT+3')))


class Bans(Base):
    __tablename__ = "bans"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    reason = Column(String)
    ending = Column(Integer)