from sqlalchemy import select, func
from db.models import User


class UserService:
    def __init__(self, session):
        self.session = session


    async def get_refferal_info(self, user_id):
        user_query = select(User).where(User.id == user_id)
        user = await self.session.scalar(user_query)
        if not user:
            return
        count = len(user.path) + 1
        parents_query = select(User).where(User.path.descendant_of(user.path),
                               func.nlevel(User.path) == count)
        parents = await self.session.scalars(parents_query)
        return parents.all()
