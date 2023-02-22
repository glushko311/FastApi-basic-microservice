import typing

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, Depends
from starlette import status

from config import JWT_SECRET, JWT_TOKEN_ALGORITHM
from src.auth.models import User
from src.auth_tools import UnathorizedException
from src.database import get_session
from src.auth.schemas import UserSchema, TokenDataSchema

if typing.TYPE_CHECKING:
    from src.auth.schemas import UserRegSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UsernameNotUniqueException(HTTPException):
    pass


class EmailNotUniqueException(HTTPException):
    pass


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_TOKEN_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise UnathorizedException()
        token_data = TokenDataSchema(username=username)
    except ExpiredSignatureError:
        raise UnathorizedException(detail="Token expired")
    except JWTError:
        raise UnathorizedException()
    user: User = await UserManager.get_by_username(db, username=token_data.username)
    if user is None:
        raise UnathorizedException()
    if user.session is None:
        raise UnathorizedException(detail="Do not have active session")
    if user.session.token != token:
        raise UnathorizedException(detail="Token invalid")
    return user


class UserManager:

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        query = await db.execute(
            select(User).where(User.username == username)
        )
        user = query.scalar()
        return user

    @staticmethod
    async def create_user(db: AsyncSession, user: 'UserRegSchema'):
        user: User = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=False,
            hashed_password=UserManager.get_password_hash(user.password),
            role_id=2
        )
        await UserManager.check_is_email_username_unique(user, db)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def check_is_email_username_unique(user: User, db: AsyncSession):
        email_check_query = \
            await db.execute(select(User.email).where(User.email == user.email))
        username_check_query = \
            await db.execute(select(User.username).where(User.username == user.username))
        if email_check_query.scalars().first():
            raise EmailNotUniqueException(status_code=400, detail="email not unique")
        if username_check_query.scalars().first():
            raise UsernameNotUniqueException(status_code=400, detail="username not unique")

    @staticmethod
    async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
        return current_user

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> typing.Union[User, bool]:

        user: User = await UserManager.get_by_username(db, username)

        if not user:
            return False
        if not UserManager.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

