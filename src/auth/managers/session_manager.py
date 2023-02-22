from datetime import datetime, timedelta
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy import delete
from src.auth.models import Session

if typing.TYPE_CHECKING:
    from src.auth.models import User


class SessionManager:
    @staticmethod
    async def update_session(db: AsyncSession, user: 'User', token: str):

        if user.session:
            await db.execute(delete(Session).where(Session.user_id == user.id))

        session: Session = Session(
            token=token,
            expired_time=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            user_id=user.id,
            user=user
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session
