from sqlalchemy import select, func
from db.models import ReferralCode

import random
import string


class RefferalCodeService:
    def __init__(self, session):
        self.session = session


    async def create(self, user, end_date):
        code = ReferralCode(code="".join(random.choices(string.ascii_lowercase, k=8)), end_date=end_date, user_id=user.id)
        self.session.add(code)


    async def refresh_code(self, user, end_date):
        new_code = "".join(random.choices(string.ascii_lowercase, k=8))
        user.referral_code.code = new_code
        user.referral_code.end_date = end_date
        self.session.add(user)
