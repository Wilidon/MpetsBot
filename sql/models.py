import time

from sqlalchemy import (Column, Integer, String,
                        BigInteger, SmallInteger)

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


class ClubUpRankHistory(Base):
    __tablename__ = "clubuprankhistory"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    owner_id = Column(Integer)
    member_id = Column(Integer)
    action = Column(String)
    date = Column(String)


class ClubAcceptPlayerHistory(Base):
    __tablename__ = "clubacceptplayerhistory"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    owner_id = Column(Integer)
    member_id = Column(Integer)
    action = Column(String)
    date = Column(String)


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


class Bans(Base):
    __tablename__ = "bans"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    reason = Column(String)
    ending = Column(Integer)