from typing import List, Optional
from sqlalchemy import UniqueConstraint, func, ForeignKey, Sequence, Column, Index
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    remote,
    foreign,
)
from sqlalchemy_utils import LtreeType, Ltree, EmailType

from datetime import date

id_seq = Sequence("users_id_seq")


class Base(DeclarativeBase):
    pass


class User(Base):
    """Таблица юзера"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(id_seq, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    path = Column(LtreeType, nullable=False)
    referral_code: Mapped["ReferralCode"] = relationship(back_populates="user", lazy="selectin")
    parent: Mapped["User"] = relationship(
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        viewonly=True,
        lazy="selectin",
    )
    __table_args__ = (Index("ix_nodes_path", path, postgresql_using="gist"),)


class ReferralCode(Base):
    '''Реферальный код'''

    __tablename__ = "referral_codes"
    id: Mapped[int] = mapped_column(id_seq, primary_key=True)
    code: Mapped[str]
    end_date: Mapped[date]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="referral_code", single_parent=True)

    __table_args__ = (UniqueConstraint("user_id"),)
