import os
import re
from sqlalchemy import select, func
from db.models import User, ReferralCode, id_seq, Ltree

from fastapi import Depends, HTTPException, status

import hashlib
from uuid import uuid4
from datetime import date


class AuthService:
    def __init__(self, session):
        self.session = session


    async def validate_registation_user(self, user):
        query = select(User.username).where(User.username == user.username)
        username = await self.session.scalar(query)
        if username:
            raise HTTPException(status_code=400, detail="Not valid username")
        query = select(User.email).where(User.email == user.email)
        email = await self.session.scalar(query)
        if email:
            raise HTTPException(status_code=400, detail="Not valid email")


    async def create_user(self, user):
        if not self.validate_email(user.email):
           raise HTTPException(status_code=400, detail="Not valid email")
        parent = None
        if user.code:
            if not await self.validate_code(user.code):
                raise HTTPException(status_code=400, detail="Not valid referral code")
            parent = await self.get_parent(user.code)
        _id = await self.session.execute(id_seq)
        ltree_id = Ltree(str(_id))
        path = ltree_id if parent is None else parent.path + ltree_id

        new_user = User(username=user.username, password=self.encrypt_password(user.password), path=path, email=user.email)
        self.session.add(new_user)


    async def validate_code(self, code):
        query = select(ReferralCode).where(ReferralCode.code == code)
        code = await self.session.scalar(query)
        if not code:
            return False
        if date.today() <= code.end_date:
            return True


    async def check_user(self, user):
        query = select(User.id).where(User.username == user.username)
        user = await self.session.scalar(query)
        return user


    async def check_password(self, user):
        query = select(User.password).where(User.username == user.username)
        password = await self.session.scalar(query)
        cipher = hashlib.new("sha256")
        cipher.update(user.password.encode())
        return cipher.hexdigest() == password


    def encrypt_password(self, password):
        cipher = hashlib.new("sha256")
        cipher.update(password.encode())
        return cipher.hexdigest()


    async def get_parent(self, code):
        query = select(User).join(ReferralCode).where(ReferralCode.code == code)
        parent = await self.session.scalar(query)
        return parent


    def validate_email(self, email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            return True
        else:
            return False
