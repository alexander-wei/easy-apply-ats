"""
Created on Aug 6, 2024

@author: alexander
"""

from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


metadata_obj = MetaData()
session_table = Table(
    "sessions",
    metadata_obj,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "memo",
        Text,
    ),
)

postings_table = Table(
    "postings",
    metadata_obj,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "title",
        String(64),
    ),
    Column(
        "company_name",
        String(128),
    ),
    Column(
        "detail",
        String(128),
    ),
    Column("session_id", Integer),
    Column(
        "url",
        String(128),
    ),
    Column(
        "description",
        Text,
    ),
    Column("date", DateTime(timezone=True), server_default=func.now()),
)

applications_table = Table(
    "applications",
    metadata_obj,
    Column("app_id", Integer, primary_key=True),
    Column("posting_id", Integer),
    Column("session_id", Integer),
    Column("date", DateTime(timezone=True), server_default=func.now()),
)


class Base(DeclarativeBase):
    pass


class Posting(Base):
    __table__ = postings_table


class UserApplication(Base):
    __table__ = applications_table
